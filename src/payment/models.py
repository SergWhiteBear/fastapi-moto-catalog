import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.dao.sql_enums import PaymentTypeEnum
from src.dao.database import Base


class Payment(Base):
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), unique=True)
    status: Mapped[PaymentTypeEnum] = mapped_column(default=PaymentTypeEnum.pending)  # pending, succeeded, failed
    order: Mapped["Order"] = relationship("Order", back_populates="payment")
