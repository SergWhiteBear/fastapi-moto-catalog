from datetime import datetime

from pydantic import BaseModel, HttpUrl, conint, confloat, Field, UUID4
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
    engine_id: str = Field(pattern=r"^[A-HJ-NPR-Z0-9]{17}$")
    frame_id: str = Field(pattern=r"^[A-HJ-NPR-Z0-9]{17}$")

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
    engine_id: str = Field(pattern=r"^[A-HJ-NPR-Z0-9]{17}$")

    class Config:
        from_attributes = True
