import random
import string
from datetime import datetime
from typing import Dict, Any, Annotated
from sqlalchemy import TIMESTAMP, func, Integer, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, relationship
from src.config import database_url

engine = create_async_engine(url=database_url)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


def generate_moto_id():
    characters = string.ascii_uppercase.replace('I', '').replace('O', '').replace('Q', '') + string.digits
    return ''.join(random.choices(characters, k=17))


uniq_str_for_moto = Annotated[str, mapped_column(unique=True, default=generate_moto_id)]
uniq_str = Annotated[str, mapped_column(unique=True)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'

    def to_dict(self) -> Dict[str, Any]:
        # Метод для преобразования объекта в словарь
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class BasketMoto(Base):
    id: Mapped[int] = mapped_column(ForeignKey("baskets.id", ondelete="CASCADE"), primary_key=True)
    moto_id: Mapped[int] = mapped_column(ForeignKey("motos.id", ondelete="CASCADE"), primary_key=True)
    basket: Mapped["Basket"] = relationship(back_populates="motos")
    moto: Mapped["Moto"] = relationship(back_populates="baskets")
