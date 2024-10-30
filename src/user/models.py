import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, ForeignKey, JSON, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from src.database import Base


class Role(Base):
    name = Column(String, nullable=False, unique=True)
    permissions = Column(JSON)

class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False, unique=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    registered_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    role = Column(String, ForeignKey('roles.name'), onupdate="CASCADE")
    hashed_password = Column(String, nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
