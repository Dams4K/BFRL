from typing import Optional

from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Players(Base):
    __tablename__ = "players"

    g_id: Mapped[int] = mapped_column(ForeignKey("guilds.g_id"), primary_key=True)
    m_id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)

class Guilds(Base):
    __tablename__ = "guilds"

    g_id: Mapped[int] = mapped_column(primary_key=True)
    update_channel_id: Mapped[int] = mapped_column(nullable=True)
    whitelist_channel_id: Mapped[int] = mapped_column(nullable=True)

class Whitelist(Base):
    __tablename__ = "whitelist"

    g_id: Mapped[int] = mapped_column(ForeignKey("guilds.g_id"), primary_key=True)
    m_id: Mapped[int] = mapped_column(primary_key=True)

class Updates(Base):
    __tablename__ = "updates"

    uuid: Mapped[str] = mapped_column(ForeignKey("players.uuid"), String(32), primary_key=True)
    next_time: Mapped[int] = mapped_column(nullable=False, default=0)

class Scores(Base):
    __tablename__  = "scores"

    uuid: Mapped[str] = mapped_column(ForeignKey("players.uuid"), String(32), primary_key=True)
    mode: Mapped[str] = mapped_column(primary_key=True)
    time_best: Mapped[int] = mapped_column(nullable=True)
    time_total: Mapped[int] = mapped_column(nullable=True)