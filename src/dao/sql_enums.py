from enum import Enum


class MotoEnum(str, Enum):
    sport = "sport"
    cross = "cross"
    enduro = "enduro"


class EngineTypeEnum(str, Enum):
    petrol_engine = "petrol"
    electric_engine = "electric"