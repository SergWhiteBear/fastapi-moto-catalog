from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.session_maker import TransactionSessionDep, SessionDep
from src.moto.dao import EngineDAO
from src.moto.schemas import SEngineBase
from src.moto.dao import MotoDAO
from fastapi import APIRouter, Depends, FastAPI
from src.moto.schemas import MotoBase


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    try:
        redis = aioredis.from_url("redis://localhost")
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
        print("Successfully connected to Redis.")
    except Exception as e:
        print(f"Error connecting to Redis: {e}")
    yield


router = APIRouter(
    prefix="/moto",
    tags=["Работа с мотоциклами"],
)

@router.post("/add_engine/", response_model=SEngineBase)
async def add_engine(engine_data: SEngineBase, session: AsyncSession = TransactionSessionDep):
    #engine = await EngineDAO.find_one_or_none(session=session, )
    engine_data_dict = engine_data.model_dump()
    engine = await EngineDAO.add(session, values=SEngineBase(**engine_data_dict))
    return engine


