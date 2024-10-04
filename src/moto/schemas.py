from pydantic import BaseModel, HttpUrl


class MotoSchema(BaseModel):
    id: int
    name: str
    price: float
    moto_class: str
    engine: str
    comments: str
    url_image: str

    class Config:
        from_attributes = True

class EngineSchema(BaseModel):
    engine_name: str
    engine_volume: int
    engine_type: str
    tact: int
    mileage: int

    class Config:
        from_attributes = True
