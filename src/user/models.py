from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.dao.database import Base


class Role(Base):
    name: Mapped[str] = mapped_column(unique=True)
    users: Mapped[list["User"]] = relationship(back_populates="role")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"

class User(Base):
    email: Mapped[str]
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), onupdate="CASCADE")
    role: Mapped["Role"] = relationship("Role", back_populates="users", lazy="joined")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

