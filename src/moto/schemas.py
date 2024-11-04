from email.policy import default

from pydantic import BaseModel, conint, Field

from src.dao.database import generate_moto_id
from src.dao.sql_enums import EngineTypeEnum, MotoEnum


class MotoBase(BaseModel):
    id: int
    frame_num: str
    name: str
    price: float
    moto_class: MotoEnum
    moto_engine_id: str
    comments: str
    url_image: list[str]

    class Config:
        from_attributes = True


class SEngineBase(BaseModel):
    id: int
    engine_num: str = Field(default=generate_moto_id())
    engine_volume: conint(gt=0)
    engine_type: EngineTypeEnum
    tact: int
    mileage: int

    class Config:
        from_attributes = True
