from typing import Optional

from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import select
from sqlalchemy import and_
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.exc import IntegrityError

from .db import engine, session

from pyplayhd import Mode

class Base(DeclarativeBase):
    @classmethod
    def add(cls, obj):
        try:
            session.add(obj)
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

    @classmethod
    def from_id(cls, g_id: int, m_id: int):
        stmt = select(Member).where(
            and_(Member.g_id == g_id, Member.m_id == m_id)
        )
        member = session.scalars(stmt).first()
        if member is None:
            member = cls(g_id=g_id, m_id=m_id)

        return member

    @classmethod
    def from_uuid(cls, g_id: int, uuid: str):
        stmt = select(Member).where(
            and_(Member.g_id == g_id, Member.uuid == uuid)
        )
        return session.scalars(stmt).first()



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
        
        return guild

class Whitelist(Base):
    __tablename__ = "whitelist"

    g_id: Mapped[int] = mapped_column(ForeignKey("guilds.g_id"), primary_key=True)
    m_id: Mapped[int] = mapped_column(primary_key=True)

class Score(Base):
    __tablename__  = "scores"

    uuid: Mapped[String] = mapped_column(String(32), ForeignKey("members.uuid"), primary_key=True)
    mode: Mapped[str] = mapped_column(primary_key=True)
    time_best: Mapped[int] = mapped_column(nullable=True)
    time_total: Mapped[int] = mapped_column(nullable=True)
    next_time: Mapped[int] = mapped_column(nullable=False, default=0)

    @classmethod
    def of_uuid(cls, uuid: str, mode: Mode):
        stmt = select(Score).where(
            and_(Score.uuid == uuid, Score.mode == str(mode))
        )
        score = session.scalars(stmt).first()
        if score is None:
            score = cls(uuid=uuid, mode=str(mode))
            cls.add(score)
        return score


Base.metadata.create_all(engine)