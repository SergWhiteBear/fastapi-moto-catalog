from pydantic import BaseModel

from src.dao.sql_enums import PaymentTypeEnum


class SPayment(BaseModel):
    id: int
    order_id: int


class SPaymentCreate(SPayment):
    status: PaymentTypeEnum
