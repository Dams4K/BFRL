import time
import discord

from typing import Optional

from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import asc
from sqlalchemy import select
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy.orm import reconstructor
from sqlalchemy.orm import aliased
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.exc import IntegrityError

from .db import engine, session

from utils.references import References
from utils.date import next_time

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



class Guild(Base):
    __tablename__ = "guilds"

    g_id: Mapped[int] = mapped_column(primary_key=True)
    update_channel_id: Mapped[int] = mapped_column(nullable=True)
    whitelist_channel_id: Mapped[int] = mapped_column(nullable=True)

    @classmethod
    def from_id(cls, g_id: int):
        stmt = select(Guild).where(Guild.g_id == g_id)
        guild = session.scalars(stmt).first()
        if guild is None:
            guild = cls(g_id=g_id)
            cls.add(guild)
        
        return guild

    def set_update_channel_id(self, value: int):
        self.update_channel_id = value
        session.commit()
    
    def set_whitelist_channel_id(self, value: int):
        self.whitelist_channel_id = value
        session.commit()

    async def fetch_whitelist_channel(self, bot: discord.Bot) -> discord.TextChannel:
        if self.whitelist_channel_id is None:
            return None

        return await bot.fetch_channel(self.whitelist_channel_id)
    async def fetch_update_channel(self, bot: discord.Bot) -> discord.TextChannel:
        if self.update_channel_id is None:
            return None
        
        return await bot.fetch_channel(self.update_channel_id)


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


class Score(Base):
    __tablename__  = "scores"

    uuid: Mapped[String] = mapped_column(String(32), ForeignKey("members.uuid"), primary_key=True)
    mode: Mapped[str] = mapped_column(primary_key=True)

    time_best: Mapped[int] = mapped_column(nullable=True)
    time_total: Mapped[int] = mapped_column(default=0)
    games: Mapped[int] = mapped_column(default=0)
    wins: Mapped[int] = mapped_column(default=0)
    confirmed: Mapped[bool] = mapped_column(default=False)
    speedrun_confirmed: Mapped[bool] = mapped_column(default=False)

    next_time: Mapped[int] = mapped_column(nullable=False, default=0)

    def update(self) -> bool:
        builder: BuilderPlayer = mcplayhd.fastbuilder.mode_player_stats(Mode[self.mode.upper()], self.uuid)
        if builder is None:
            return False
        
        stats: BuilderStats = builder.builder_stats
        if stats is None:
            return False
        
        time_improved = False
        if stats.time_best > 0:
            time_improved = self.time_best != stats.time_best
            self.time_best = stats.time_best
        
        self.time_total = stats.time_total
        self.games = stats.games
        self.wins = stats.wins
        self.confirmed = stats.confirmed
        self.speedrun_confirmed = stats.speedrun_confirmed

        self.next_time = next_time(int(time.time()), self.mode)

        session.commit()

        return time_improved

    def __repr__(self):
        return f"<{self.__class__.__name__} uuid={self.uuid} time_best={self.time_best} time_total={self.time_total} next_time={self.next_time}>"
    
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
    def get_leaderboard_query(mode: Mode):
        sub_query = session.query(Score)
        sub_query = sub_query.join(Member, Score.uuid == Member.uuid)
        sub_query = sub_query.join(Whitelist, and_(Whitelist.g_id == Member.g_id, Whitelist.m_id == Member.m_id))
        sub_query = sub_query.filter(Score.mode == str(mode))
        sub_query = sub_query.filter(Score.time_best != None)

        row_number = func.row_number().over(order_by=asc(Score.time_best)).label("rank")
        sub_query = sub_query.add_column(row_number)
        return sub_query


    @staticmethod
    def get_leaderboard(mode: Mode):
        return session.execute(Score.get_leaderboard_query(mode)).all()
    
    def get_rank(self) -> int | None:
        # I'd love using a filter, but row_number keep being updated and always return 1, and because i didn't find any information online, i'm force to do this shit
        lb = Score.get_leaderboard(self.mode)
        for score, rank in lb:
            if score.uuid == self.uuid:
                return rank
        return None


Base.metadata.create_all(engine)