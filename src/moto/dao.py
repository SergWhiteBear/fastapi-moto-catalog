from src.dao.base import BaseDAO
from src.moto.models import Moto, Engine


class MotoDAO(BaseDAO):
    model = Moto

class EngineDAO(BaseDAO):
    model = Engine