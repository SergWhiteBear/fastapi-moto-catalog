from sqlalchemy import (
    Column, Integer, Float,
    String, Text, ForeignKey)
from src.database import Base


class Engine(Base):
    id = Column(String(17), unique=True, primary_key=True)
    engine_volume = Column(Integer, nullable=False)
    engine_type = Column(String(255), nullable=False)
    tact = Column(Integer, nullable=False)
    mileage = Column(Integer, nullable=False)


class Moto(Base):
    id = Column(String(17), unique=True, primary_key=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    moto_class = Column(String(255), nullable=False)
    engine_id = Column(String(17), ForeignKey('engines.id'), nullable=False)
    comments = Column(Text, nullable=False)
    url_image = Column(String(255), nullable=True)
