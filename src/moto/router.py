from contextlib import asynccontextmanager
from functools import wraps
from typing import Callable, Any

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import *
from src.dao.session_maker import TransactionSessionDep, SessionDep
from src.moto.dao import EngineDAO, MotoDAO
from src.moto.schemas import SEngineWrite, SEngineRead, EngineModel, SMotoRead, MotoModel, SMotoWrite, \
    SEngineUpdate, SMotoUpdate, SMotoFilter
from fastapi import APIRouter, FastAPI, HTTPException, Depends


def handle_dao_errors(func: Callable) -> Callable:
    """
    Декоратор для обработки ошибок DAO и стандартизации ответов.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except HTTPException:
            raise  # Пробрасываем HTTPException, чтобы FastAPI мог обработать его
        except Exception as e:
            raise InternalServerErrorException

    return wrapper


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


@router.post("/add_engine/", response_model=SEngineRead)
@handle_dao_errors
async def add_engine(engine_data: SEngineWrite, session: AsyncSession = TransactionSessionDep):
    engine = await EngineDAO.find_one_or_none(session=session, filters=EngineModel(engine_num=engine_data.engine_num))
    if engine:
        raise EngineAlreadyExistsException

    engine_data_dict = engine_data.model_dump()
    engine = await EngineDAO.add(session, values=SEngineWrite(**engine_data_dict))
    return engine


# Убрать или оставить только для админа
@router.get("/get_engine/", response_model=SEngineRead)
@handle_dao_errors
async def get_engine(engine_num: str, session: AsyncSession = SessionDep):
    engine = await EngineDAO.find_one_or_none(session=session, filters=EngineModel(engine_num=engine_num))
    if not engine:
        raise EngineNotFoundException
    return engine


@router.patch("/update_engine/")
@handle_dao_errors
async def update_engine(update_data: SEngineUpdate, filters: SEngineUpdate = Depends(),
                        session: AsyncSession = TransactionSessionDep):
    updated_rows = await EngineDAO.update(session, filters=filters, values=update_data)
    if updated_rows == 0:
        raise NoRecordsFoundException
    return updated_rows


@router.delete("/delete_engine/")
@handle_dao_errors
async def delete_engine(filters: SEngineUpdate = Depends(), session: AsyncSession = TransactionSessionDep):
    deleted_rows = await EngineDAO.delete(session, filters=filters)
    if deleted_rows == 0:
        raise NoRecordsFoundException
    return deleted_rows


@router.get("/get_all_engine/")
@handle_dao_errors
async def get_all_engine(filters: SEngineUpdate = Depends(), session: AsyncSession = SessionDep):
    all_rows = await EngineDAO.get_all(session, filters=filters)
    if not all_rows:
        raise EngineNotFoundException
    return all_rows


@router.get("/get_engine/{id}")
@handle_dao_errors
async def get_engine_by_id(id_: int, session: AsyncSession = SessionDep):
    engine = await EngineDAO.find_one_or_none_by_id(session=session, data_id=id_)
    if not engine:
        raise EngineNotFoundException
    return engine


@router.post("/add_moto/", response_model=SMotoWrite)
@handle_dao_errors
async def add_moto(moto_data: SMotoWrite, session: AsyncSession = TransactionSessionDep):
    moto = await MotoDAO.find_one_or_none(session=session, filters=MotoModel(frame_num=moto_data.frame_num))
    if moto:
        raise MotoAlreadyExistsException

    moto_data_dict = moto_data.model_dump()
    moto = await MotoDAO.add(session, values=SMotoWrite(**moto_data_dict))
    return moto


@router.get("/get_moto/", response_model=SMotoRead)
@handle_dao_errors
async def get_moto(frame_num: str, session: AsyncSession = SessionDep):
    moto = await MotoDAO.find_one_or_none(session=session, filters=MotoModel(frame_num=frame_num))
    if not moto:
        raise MotoNotFoundException
    return moto


@router.patch("/update_moto/")
@handle_dao_errors
async def update_moto(update_data: SMotoUpdate, filters: SMotoUpdate = Depends(),
                      session: AsyncSession = TransactionSessionDep):
    updated_rows = await MotoDAO.update(session, filters=filters, values=update_data)
    if updated_rows == 0:
        raise NoRecordsFoundException
    return updated_rows


@router.delete("/delete_moto/")
@handle_dao_errors
async def delete_moto(filters: SMotoUpdate = Depends(), session: AsyncSession = TransactionSessionDep):
    deleted_rows = await MotoDAO.delete(session, filters=filters)
    if deleted_rows == 0:
        raise NoRecordsFoundException
    return deleted_rows


@router.get("/get_all_moto/")
@handle_dao_errors
async def get_all_moto(filters: SMotoFilter = Depends(), session: AsyncSession = SessionDep):
    all_rows = await MotoDAO.get_all(session, filters=filters)
    if not all_rows:
        raise MotoNotFoundException
    return all_rows


@router.get("/get_moto/{id}")
@handle_dao_errors
async def get_moto_by_id(id_: int, session: AsyncSession = SessionDep):
    moto = await MotoDAO.find_one_or_none_by_id(session=session, data_id=id_)
    if not moto:
        raise MotoNotFoundException
    return moto
