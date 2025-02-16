from pydantic import BaseModel, Field, ConfigDict

from src.dao.database import generate_moto_id
from src.dao.sql_enums import EngineTypeEnum, MotoEnum


class EngineModel(BaseModel):
    engine_num: str = Field(default=generate_moto_id())
    model_config = ConfigDict(from_attributes=True)


class MotoModel(BaseModel):
    frame_num: str = Field(default=generate_moto_id())
    model_config = ConfigDict(from_attributes=True)


class SMotoFilter(BaseModel):
    frame_num: str | None = None
    name: str | None = None
    price: float | None = None
    moto_class: MotoEnum | None = None


class SMotoUpdate(SMotoFilter):
    pass


class SEngineWrite(EngineModel):
    engine_volume: int
    engine_type: EngineTypeEnum
    tact: int
    mileage: int


class SEngineUpdate(BaseModel):
    engine_num: str | None = None
    engine_volume: int | None = None
    engine_type: EngineTypeEnum | None = None
    tact: int | None = None
    mileage: int | None = None


class SEngineRead(SEngineWrite):
    id: int = Field(..., exclude=True)
    engine_num: str = Field(default=generate_moto_id(), exclude=True)


class SMotoWrite(MotoModel):
    name: str
    price: float
    moto_class: MotoEnum
    engine_id: int
    comments: str
    image_url: list[str]


class SMotoRead(SMotoWrite):
    id: int = Field(..., exclude=True)
    frame_num: str = Field(default=generate_moto_id(), exclude=True)
    engine: SEngineRead
    image_url: list[str] = Field(exclude=True)
