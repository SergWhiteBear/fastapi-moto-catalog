from pydantic import BaseModel, conint, confloat, Field
from typing import Literal


class MotoBase(BaseModel):
    name: str
    price: confloat(gt=0)
    moto_class: str
    comments: str
    url_image: str

    class Config:
        from_attributes = True


class MotoWrite(MotoBase):
    engine_id: str = Field(
        "(your engine id value)",
        pattern=r"^[A-HJ-NPR-Z0-9]{17}$",
        description="Идентификатор двигателя (17 символов, без букв I, O, Q)"
    )

    id: str = Field(
        "(your moto frame id value)",
        pattern=r"^[A-HJ-NPR-Z0-9]{17}$",
        description="Уникальный идентификатор мотоцикла (17 символов, без букв I, O, Q)"
    )

    class Config:
        from_attributes = True


class EngineBase(BaseModel):
    engine_volume: conint(gt=0)
    engine_type: Literal['бензиновый', 'электрический']
    tact: int
    mileage: int

    class Config:
        from_attributes = True


class EngineWrite(EngineBase):
    engine_id: str = Field(
        "(your engine id value)",
        pattern=r"^[A-HJ-NPR-Z0-9]{17}$",
        description="Идентификатор двигателя (17 символов, без букв I, O, Q)"
    )

    class Config:
        from_attributes = True
