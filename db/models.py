import time
import discord
import string

from typing import Optional

from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import asc
from sqlalchemy import select
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.exc import IntegrityError

from .db import engine, session

from utils.references import References
from utils.date import next_time
from utils.format import FormatDict

from pyplayhd import *
from mcapi.player import get_name

mcplayhd = Client(References.MCPLAYHD_TOKEN)

class Base(DeclarativeBase):
    @classmethod
    def add(cls, obj):
        try:
            session.add(obj)
            session.commit()
        except IntegrityError:
            session.rollback()
    
    @classmethod
    def delete(cls, obj):
        if obj is None:
            return
        try:
            session.delete(obj)
            session.commit()
        except IntegrityError:
            session.rollback()


class Member(Base):
    __tablename__ = "members"

    g_id: Mapped[int] = mapped_column(ForeignKey("guilds.g_id"), primary_key=True)
    m_id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[Optional[String]] = mapped_column(String(32), nullable=True)

    def get_scores(self):
        stmt = select(Score).where(Score.uuid == self.uuid)
        return session.scalars(stmt)
    
    def get_score(self, mode: Mode):
        return Score.of_uuid(self.uuid, mode)

    def set_uuid(self, value: str):
        self.uuid = value
        self.create_scores()
        session.commit()
    
    def as_whitelist(self):
        return Whitelist(g_id=self.g_id, m_id=self.m_id)

    def whitelist(self):
        self.add(self.as_whitelist())
    def unlist(self):
        Whitelist.unlist(self.g_id, self.m_id)

    async def fetch_user(self, bot: discord.Bot) -> discord.User:
        return await bot.fetch_user(self.m_id)
    
    def get_name(self) -> str:
        return get_name(self.uuid)

    @classmethod
    def from_id(cls, g_id: int, m_id: int):
        stmt = select(Member).where(
            and_(Member.g_id == g_id, Member.m_id == m_id)
        )
        member = session.scalars(stmt).first()
        if member is None:
            member = cls(g_id=g_id, m_id=m_id)
            cls.add(member)

        return member

    @classmethod
    def from_uuid(cls, g_id: int, uuid: str):
        stmt = select(Member).where(
            and_(Member.g_id == g_id, Member.uuid == uuid)
        )
        return session.scalars(stmt).first()
    
    def create_scores(self):
        if self.uuid is None:
            return
        for mode in Mode:
            self.add(Score.of_uuid(self.uuid, mode))


class Score(Base):
    __tablename__  = "scores"

    uuid: Mapped[String] = mapped_column(String(32), ForeignKey("members.uuid"), primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    group: Mapped[str] = mapped_column(nullable=True)
    mode: Mapped[str] = mapped_column(primary_key=True)

    time_best: Mapped[int] = mapped_column(nullable=True)
    time_total: Mapped[int] = mapped_column(default=0)
    games: Mapped[int] = mapped_column(default=0)
    wins: Mapped[int] = mapped_column(default=0)
    confirmed: Mapped[bool] = mapped_column(default=False)
    speedrun_confirmed: Mapped[bool] = mapped_column(default=False)

    next_time: Mapped[int] = mapped_column(nullable=False, default=0)

    def update(self):
        builder: BuilderPlayer = mcplayhd.fastbuilder.mode_player_stats(Mode[self.mode.upper()], self.uuid)
        if builder is None:
            return
        
        stats: BuilderStats = builder.builder_stats
        if stats is None:
            return
        
        if stats.time_best > 0:
            self.time_best = stats.time_best
        
        self.time_total = stats.time_total
        self.games = stats.games
        self.wins = stats.wins
        self.confirmed = stats.confirmed
        self.speedrun_confirmed = stats.speedrun_confirmed

        self.next_time = next_time(int(time.time()), self.mode)

        if player_info := builder.player_info:
            self.name = player_info.name
            self.group = player_info.group

        session.commit()

    def __repr__(self):
        return f"<{self.__class__.__name__} uuid={self.uuid} time_best={self.time_best} time_total={self.time_total} next_time={self.next_time}>"
    
    def as_user_id(self, g_id: int) -> int:
        stmt = select(Member.m_id).join(Score, Score.uuid == Member.uuid).where(Score.mode == self.mode).where(and_(Member.g_id == g_id, Member.uuid == self.uuid))
        return session.scalars(stmt).first()

    def get_name(self):
        if self.name is None:
            self.name = get_name(self.uuid)
            session.commit()
        return self.name or "Unknown"

    @staticmethod
    def of_uuid(uuid: str, mode: Mode):
        stmt = select(Score).where(
            and_(Score.uuid == uuid, Score.mode == str(mode))
        )
        score = session.scalars(stmt).first()
        if score is None:
            score = Score(uuid=uuid, mode=str(mode))
            Score.add(score)
        return score
    

    @staticmethod
    def to_update():
        current_time: int = int(time.time())

        stmt = select(Score).where(Score.next_time <= current_time).order_by(asc(Score.next_time)).limit(60)
        return session.scalars(stmt).all()


    @staticmethod
    def get_leaderboard_query(mode: Mode, guild_id: int = 1017489023842930700): #TODO: this is hardcoded because i have only one sheet manually created
        sub_query = session.query(Score)
        sub_query = sub_query.join(Member, and_(Score.uuid == Member.uuid, Member.g_id == guild_id))
        sub_query = sub_query.join(Whitelist, and_(Whitelist.g_id == Member.g_id, Whitelist.m_id == Member.m_id))
        sub_query = sub_query.filter(Score.mode == str(mode))
        sub_query = sub_query.filter(Score.time_best != None)

        row_number = func.row_number().over(order_by=asc(Score.time_best)).label("rank")
        sub_query = sub_query.add_column(row_number)
        return sub_query


    @staticmethod
    def get_leaderboard(mode: Mode, guild_id: int = 1017489023842930700):
        return session.execute(Score.get_leaderboard_query(mode, guild_id)).all()
    
    def get_rank(self) -> int | None:
        # I'd love using a filter, but row_number keep being updated and always return 1, and because i didn't find any information online, i'm force to do this shit
        lb = Score.get_leaderboard(self.mode)
        for score, rank in lb:
            if score.uuid == self.uuid:
                return rank
        return None
    
    def get_affected_guilds(self):
        stmt = (select(Guild.g_id)
                .join(Member, Member.uuid == self.uuid)
                .join(Whitelist, Whitelist.g_id == Member.g_id)
                .group_by(Guild.g_id)
        )
        return session.execute(stmt).all()

    async def send_new_rank(self, bot: discord.Bot, old_time: int, old_rank: int):
        for guild_info in self.get_affected_guilds():
            if len(guild_info) == 0:
                continue

            guild_id = guild_info[0]
            dguild: Guild = Guild.from_id(guild_id)
            await dguild.send_rank_message(bot, self, old_time, old_rank)

    async def send_new_time(self, bot: discord.Bot, old_time: int, old_rank: int):
        for guild_info in self.get_affected_guilds():
            if len(guild_info) == 0:
                continue

            guild_id = guild_info[0]
            dguild: Guild = Guild.from_id(guild_id)
            await dguild.send_time_message(bot, self, old_time, old_rank)


class Guild(Base):
    __tablename__ = "guilds"

    g_id: Mapped[int] = mapped_column(primary_key=True)
    
    update_channel_id: Mapped[int] = mapped_column(nullable=True)
    time_message: Mapped[str] = mapped_column(nullable=True, default="New pb of {time:.3f}s for {member.mention} in {mode}! `#{rank}`")
    rank_message: Mapped[str] = mapped_column(nullable=True, default="New rank in {mode} for {member.mention}! `#{old_rank} → #{rank}` with a time of {time:.3f}s")

    whitelist_channel_id: Mapped[int] = mapped_column(nullable=True)
    required_role_id: Mapped[int] = mapped_column(nullable=True)

    @classmethod
    def from_id(cls, g_id: int):
        stmt = select(Guild).where(Guild.g_id == g_id)
        guild = session.scalars(stmt).first()
        if guild is None:
            guild = cls(g_id=g_id)
            cls.add(guild)
        
        return guild

    def set_update_channel(self, channel: discord.TextChannel):
        if channel is None:
            return

        self.update_channel_id = channel.id
        session.commit()
    
    def set_whitelist_channel(self, channel: discord.TextChannel):
        if channel is None:
            return

        self.whitelist_channel_id = channel.id
        session.commit()

    def set_link_required_role(self, role: discord.Role):
        if role is None:
            return

        self.required_role_id = role.id
        session.commit()

    def set_rank_message(self, message):
        self.rank_message = message
        session.commit()
    def set_time_message(self, message):
        self.time_message = message
        session.commit()

    async def fetch_whitelist_channel(self, bot: discord.Bot) -> discord.TextChannel:
        if self.whitelist_channel_id is None:
            return None

        return await bot.fetch_channel(self.whitelist_channel_id)
    async def fetch_update_channel(self, bot: discord.Bot) -> discord.TextChannel:
        if self.update_channel_id is None:
            return None
        
        return await bot.fetch_channel(self.update_channel_id)
    
    def get_required_role(self, bot: discord.Bot) -> discord.Role:
        if self.required_role_id is None:
            return None
        
        return bot.get_guild(self.g_id).get_role(self.required_role_id)
    
    async def send_time_message(self, bot: discord.Bot, score: Score, old_time: int, old_rank: int):
        user_id = score.as_user_id(self.g_id)
        if user_id is None:
            return

        user: discord.User = await bot.fetch_user(user_id)
        if user is None:
            return
        
        d = FormatDict({
            "mode": str(score.mode),
            "time": score.time_best/1000,
            "old_time": old_time/1000,
            "rank": score.get_rank(),
            "old_rank": old_rank,
            "member": user
        })
        formatter = string.Formatter()
        message = formatter.vformat(self.time_message, (), d)
        await self.send_update_message(bot, message)
        
    
    async def send_rank_message(self, bot: discord.Bot, score: Score, old_time: int, old_rank: int):
        user_id = score.as_user_id(self.g_id)
        if user_id is None:
            return

        user: discord.User = await bot.fetch_user(user_id)
        if user is None:
            return

        d = FormatDict({
            "mode": str(score.mode),
            "time": score.time_best,
            "old_time": old_time,
            "rank": score.get_rank(),
            "old_rank": old_rank,
            "member": user
        })
        formatter = string.Formatter()
        message = formatter.vformat(self.rank_message, (), d)
        await self.send_update_message(bot, message)
    
    async def send_update_message(self, bot: discord.Bot, message: str):
        update_channel: discord.TextChannel = await self.fetch_update_channel(bot)
        if update_channel is None:
            return
        await update_channel.send(message)



class Whitelist(Base):
    __tablename__ = "whitelist"

    g_id: Mapped[int] = mapped_column(ForeignKey("guilds.g_id"), primary_key=True)
    m_id: Mapped[int] = mapped_column(primary_key=True)


    @classmethod
    def whitelist(cls, g_id: int, m_id: int):
        cls.add(cls(g_id=g_id, m_id=m_id))
    
    @classmethod
    def unlist(cls, g_id: int, m_id: int):
        stmt = select(Whitelist).where(
            and_(Whitelist.g_id == g_id, Whitelist.m_id == m_id)
        )
        cls.delete(session.scalars(stmt).first())



Base.metadata.create_all(engine)