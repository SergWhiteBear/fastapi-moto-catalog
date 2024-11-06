from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.session_maker import TransactionSessionDep, SessionDep
from src.moto.dao import EngineDAO, MotoDAO
from src.moto.schemas import SEngineWrite, SEngineRead, EngineModel, SMotoRead, MotoModel, SMotoWrite, \
    SEngineUpdate, SEngineFilter, SMotoUpdate, SMotoFilter
from fastapi import APIRouter, FastAPI, HTTPException, status, Depends


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
async def add_engine(engine_data: SEngineWrite, session: AsyncSession = TransactionSessionDep):
    engine = await EngineDAO.find_one_or_none(session=session, filters=EngineModel(engine_num=engine_data.engine_num))
    if engine:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Запись с таким номером двигателя уже существует")
    engine_data_dict = engine_data.model_dump()
    engine = await EngineDAO.add(session, values=SEngineWrite(**engine_data_dict))
    return engine


@router.get("/get_engine/", response_model=SEngineRead)
async def get_engine(engine_num, session: AsyncSession = SessionDep):
    engine = await EngineDAO.find_one_or_none(session=session, filters=EngineModel(engine_num=engine_num))
    if not engine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return engine


@router.patch("/update_engine/")
async def update_engine(update_data: SEngineUpdate, filters: SEngineUpdate = Depends(),
                        session: AsyncSession = TransactionSessionDep):
    updated_rows = await EngineDAO.update(session, filters=filters,
                                          values=update_data)
    if updated_rows == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Записей для обновления не было найдено")
    return updated_rows


@router.delete("/delete_engine/")
async def delete_engine(filters: SEngineUpdate = Depends(), session: AsyncSession = TransactionSessionDep):
    deleted_rows = await EngineDAO.delete(session, filters=filters)
    if deleted_rows == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не удалось найти записей для удаления")
    return deleted_rows

@router.get("/get_all_engine/")
async def get_all_engine(filters: SEngineFilter = Depends(), session: AsyncSession = SessionDep):
    all_rows = await EngineDAO.get_all(session, filters=filters)
    if not all_rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return all_rows

@router.get("/get_engine/{id}")
async def get_engine_by_id(id: int, session: AsyncSession = SessionDep):
    engine = await EngineDAO.find_one_or_none_by_id(session=session, data_id=id)
    if not engine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return engine

@router.post("/add_moto/", response_model=SMotoRead)
async def add_moto(moto_data: SMotoWrite, session: AsyncSession = TransactionSessionDep):
    moto = await MotoDAO.find_one_or_none(session=session, filters=MotoModel(frame_num=moto_data.frame_num))
    if moto:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Данный мотоцикл уже существует в базе")
    moto_data_dict = moto_data.model_dump()
    moto = await MotoDAO.add(session, values=SMotoWrite(**moto_data_dict))
    return moto


@router.get("/get_moto/", response_model=SMotoRead)
async def get_moto(frame_num, session: AsyncSession = SessionDep):
    moto = await MotoDAO.find_one_or_none(session=session, filters=MotoModel(frame_num=frame_num))
    if not moto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return moto

@router.patch("/update_moto/")
async def update_moto(update_data: SMotoUpdate, filters: SMotoUpdate = Depends(),
                        session: AsyncSession = TransactionSessionDep):
    updated_rows = await MotoDAO.update(session, filters=filters,
                                          values=update_data)
    if updated_rows == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Записей для обновления не было найдено")
    return updated_rows


@router.delete("/delete_moto/")
async def delete_moto(filters: SMotoUpdate = Depends(), session: AsyncSession = TransactionSessionDep):
    deleted_rows = await MotoDAO.delete(session, filters=filters)
    if deleted_rows == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не удалось найти записей для удаления")
    return deleted_rows

@router.get("/get_all_moto/")
async def get_all_moto(filters: SMotoFilter = Depends(), session: AsyncSession = SessionDep):
    all_rows = await MotoDAO.get_all(session, filters=filters)
    if not all_rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return all_rows

@router.get("/get_moto/{id}")
async def get_moto_by_id(id: int, session: AsyncSession = SessionDep):
    moto = await MotoDAO.find_one_or_none_by_id(session=session, data_id=id)
    if not moto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return moto