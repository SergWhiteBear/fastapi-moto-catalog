from typing import List

from sqlalchemy import ForeignKey, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.dao.sql_enums import OrderEnum
from src.dao.database import Base


class Basket(Base):
    user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), unique=True,
                                                nullable=True)
    guest_id: Mapped[str | None] = mapped_column(unique=True,
                                                 nullable=True)  # временный идентификатор для гостей

    motos: Mapped[List["BasketMoto"]] = relationship(back_populates="basket")


class Order(Base):
    user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), unique=True,
                                                nullable=True)
    guest_id: Mapped[str | None] = mapped_column(unique=True, nullable=True)  # для гостевых пользователей
    status: Mapped[OrderEnum] = mapped_column(default=OrderEnum.pending)
    total_price: Mapped[float] = mapped_column(Float, default=0.0)

    user: Mapped["User"] = relationship("User", back_populates="orders")
    basket_items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    moto_id: Mapped[int] = mapped_column(ForeignKey('motos.id'))
    quantity: Mapped[int] = mapped_column(Integer, default=1)

    order: Mapped["Order"] = relationship("Order", back_populates="basket_items")
    moto: Mapped["Moto"] = relationship("Moto")
