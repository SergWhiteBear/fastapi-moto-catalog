from sqlalchemy import Text, ARRAY, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.dao.sql_enums import EngineTypeEnum, MotoEnum
from src.dao.database import Base, uniq_str_for_moto


class Engine(Base):
    engine_num: Mapped[uniq_str_for_moto]
    engine_volume: Mapped[int]
    engine_type: Mapped[EngineTypeEnum] = mapped_column(
        default=EngineTypeEnum.petrol_engine,
        nullable=False)
    tact: Mapped[int]
    mileage: Mapped[int]
    moto: Mapped["Moto"] = relationship("Moto", back_populates="engine")


class Moto(Base):
    frame_num: Mapped[uniq_str_for_moto]
    name: Mapped[str]
    price: Mapped[float]
    moto_class: Mapped[MotoEnum] = mapped_column(
        default=MotoEnum.cross,
        nullable=False)
    engine_num: Mapped[str] = mapped_column(ForeignKey('engines.engine_num'))
    engine: Mapped["Engine"] = relationship(
        "Engine",
        back_populates="moto",
    )
    comments: Mapped[str | None] = mapped_column(Text)
    image_url: Mapped[list[str] | None] = mapped_column(ARRAY(String))
