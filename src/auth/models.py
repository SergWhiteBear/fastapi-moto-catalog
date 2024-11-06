from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.dao.database import Base, uniq_str


class Role(Base):
    name: Mapped[uniq_str] = mapped_column(unique=True)
    users: Mapped[list["User"]] = relationship(back_populates="role")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"

class User(Base):
    email: Mapped[uniq_str]
    phone_num: Mapped[uniq_str]
    username: Mapped[uniq_str]
    password: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), default=1, onupdate="CASCADE")
    role: Mapped["Role"] = relationship("Role", back_populates="users", lazy="joined")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"

