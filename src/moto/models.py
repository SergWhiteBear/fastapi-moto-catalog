from datetime import datetime, timezone
import uuid
from sqlalchemy import (
    Table, Column, Integer, Float,
    String, Text, DateTime, ForeignKey, MetaData)
from sqlalchemy.dialects.postgresql import UUID
from src.database import Base

metadata = MetaData()

engine = Table(
    "engine",
    metadata,
    Column("uuid", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("engine_id", String(17), unique=True),
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
    Column("uuid", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("frame_id",String(17), unique=True),
    Column("name", String(255), nullable=False),
    Column("price", Float, nullable=False),
    Column("moto_class", String(255), nullable=False),
    Column("engine_id", String(17), ForeignKey('engine.engine_id'), nullable=False),
    Column("comments", Text, nullable=False),
    Column("url_image", String(255), nullable=True),
    Column("created_at", DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False),
    Column("updated_at", DateTime(timezone=True), default=datetime.now(timezone.utc),
           onupdate=datetime.now(timezone.utc), nullable=False),
)


class Moto(Base):
    __tablename__ = "moto"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    frame_id = Column(String(17), unique=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    moto_class = Column(String(255), nullable=False)
    engine_name = Column(String(17), ForeignKey('engine.engine_id'), nullable=False)
    comments = Column(Text, nullable=False)
    url_image = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc),
                        onupdate=datetime.now(timezone.utc), nullable=False)


class Engine(Base):
    __tablename__ = "engine"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    engine_id = Column(String(17), unique=True)
    engine_volume = Column(Integer, nullable=False)
    engine_type = Column(String(255), nullable=False)
    tact = Column(Integer, nullable=False)
    mileage = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc),
                        onupdate=datetime.now(timezone.utc), nullable=False)
