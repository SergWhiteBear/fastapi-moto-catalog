from enum import Enum


class MotoEnum(str, Enum):
    sport = "sport"
    cross = "cross"
    enduro = "enduro"


class EngineTypeEnum(str, Enum):
    petrol_engine = "petrol"
    electric_engine = "electric"

class OrderEnum(str, Enum):
    pending = "pending"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    completed = "completed"
    canceled = "canceled"
    failed = "failed"
    on_hold = "on_hold"
    awaiting_payment = "awaiting_payment"
    paid = "paid"
    backordered = "backordered"
    partial_shipped = "partial_shipped"

class PaymentTypeEnum(str, Enum):
    pending = "pending"
    success = "success"
    failure = "failure"