from pydantic import BaseModel, Field

from src.moto.schemas import SMotoRead


class BasketModel(BaseModel):
    user_id: int | None = None
    guest_id: str | None = None  # временный идентификатор для гостей


class BasketMotoModel(BaseModel):
    id: int | None = None
    moto_id: int | None = None


class BasketReadModel(BasketMotoModel):
    basket: BasketModel
    moto: SMotoRead

class OrderModel(BasketModel):
    status: str = Field(default='pending')
    total_price: float = Field(default=0.0)

class OrderFilter(BaseModel):
    id: int | None = None
    user_id: int | None = None
    guest_id: str | None = None
    status: str | None = None
    total_price: float | None = None

class OrderMotoModel(BaseModel):
    order_id: int
    moto_id: int
    quantity: int = Field(default=1)