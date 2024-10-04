from datetime import datetime, timezone

from sqlalchemy import (
    Table, Column, Integer, Float, MetaData,
    String, Text, DateTime, ForeignKey)

from src.database import Base

metadata = MetaData()

engine = Table(
    "engine",
    metadata,
    Column("engine_name", String(255), primary_key=True),
    Column("engine_volume", Integer, nullable=False),
    Column("engine_type", String(255), nullable=False),
    Column("tact", Integer, nullable=False),
    Column("mileage", Integer, nullable=False),
    Column("created_at", DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False),
    Column("updated_at", DateTime(timezone=True), default=datetime.now(timezone.utc),
           onupdate=datetime.now(timezone.utc), nullable=False),
)

moto = Table(
    "moto",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(255), nullable=False),
    Column("price", Float, nullable=False),
    Column("moto_class", String(255), nullable=False),
    Column("engine", String(255), ForeignKey('engine.engine_name'), nullable=False, unique=True),
    Column("comments", Text, nullable=False),
    Column("url_image", String(255), nullable=True),
    Column("created_at", DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False),
    Column("updated_at", DateTime(timezone=True), default=datetime.now(timezone.utc),
           onupdate=datetime.now(timezone.utc), nullable=False),
)


class Moto(Base):
    __tablename__ = "moto"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    moto_class = Column(String(255), nullable=False)
    engine = Column(String(255), ForeignKey('engine.name'), nullable=False, unique=True)
    comments = Column(Text, nullable=False)
    url_image = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)


class Engine(Base):
    __tablename__ = "engine"
    engine_name = Column(String(255), nullable=False, primary_key=True)
    engine_volume = Column(Integer, nullable=False)
    engine_type = Column(String(255), nullable=False)
    tact = Column(Integer, nullable=False)
    mileage = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
