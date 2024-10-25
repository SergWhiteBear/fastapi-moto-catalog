import uuid
from datetime import datetime, timezone

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Column, String, ForeignKey, JSON, Boolean, MetaData, DateTime
from sqlalchemy.dialects.postgresql import UUID
from src.database import Base

metadata = MetaData()

role = Table(
    "role",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("name", String, nullable=False, unique=True),
    Column("permissions", JSON),
)

user = Table(
    "user",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("registered_at", DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False),
    Column("role", String, ForeignKey(role.c.name), onupdate="CASCADE"),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)


class User(SQLAlchemyBaseUserTable[UUID], Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False, unique=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    registered_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    role = Column(String, ForeignKey(role.c.name), onupdate="CASCADE")
    hashed_password = Column(String, nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
