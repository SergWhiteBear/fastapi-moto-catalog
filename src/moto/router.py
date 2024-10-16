from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from src.database import get_async_session
from fastapi import APIRouter, Depends, HTTPException
from src.moto.models import moto, engine, Engine, Moto
from src.moto.schemas import MotoBase, EngineBase, EngineWrite, MotoWrite
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(
    prefix="/moto",
    tags=["moto"],
)


async def delete_model(model, model_id, session: AsyncSession = Depends(get_async_session)) -> dict[str, Any]:
    existing_object = await session.get(model, model_id)
    if not existing_object:
        raise HTTPException(status_code=404, detail="Not Found")
    await session.delete(existing_object)
    await session.commit()
    return {"status": 200, "msg": "Deleted Successfully"}

async def update_model(model, model_update, model_id, session: AsyncSession = Depends(get_async_session)) -> dict:
    existing_object = await session.get(model, model_id)
    if not existing_object:
        raise HTTPException(status_code=404, detail="Not Found")
    for key, value in model_update.model_dump().items():
        setattr(existing_object, key, value)
    await session.commit()
    await session.refresh(existing_object)
    return {"updated_object": existing_object}


@router.get("/get_engine")
async def get_engine(
        engine_id: str,
        session: AsyncSession = Depends(get_async_session)
) -> dict[str, EngineBase]:
    try:
        existing_engine = await session.get(Engine, engine_id)
        if existing_engine:
            return {f"{engine_id}": EngineBase.model_validate(existing_engine)}
        raise HTTPException(status_code=404, detail="Not Found")
    except SQLAlchemyError as db_error:
        await session.rollback()
        raise SQLAlchemyError(f"Database error: {db_error}")


@router.post("/add_engine")
async def add_engine(
        new_engine: EngineWrite,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        stmt = insert(engine).values(**new_engine.model_dump())
        await session.execute(stmt)
        await session.commit()
        return {"result": 200}
    except SQLAlchemyError as db_error:
        await session.rollback()
        raise SQLAlchemyError(f"Database error: {db_error}")


@router.put("/update_engine")
async def update_engine(
        engine_id: str,
        engine_update: EngineWrite,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        responses = await update_model(Engine, engine_update, engine_id, session)
        return responses
    except SQLAlchemyError as db_error:
        await session.rollback()
        raise SQLAlchemyError(f"Database error: {db_error}")


@router.delete("/delete_engine")
async def delete_engine(
        engine_id: str,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        response = await delete_model(engine, engine_id, session)
        return response
    except SQLAlchemyError as db_error:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {db_error}")


@router.get("/get_moto")
async def get_moto(
        frame_id: str,
        session: AsyncSession = Depends(get_async_session)
) -> dict[str, MotoBase]:
    try:
        existing_moto = await session.get(Moto, frame_id)
        if existing_moto:
            return {f"{frame_id}": MotoBase.model_validate(existing_moto)}
        raise HTTPException(status_code=404, detail="Moto not found")
    except SQLAlchemyError as db_error:
        await session.rollback()
        raise SQLAlchemyError(f"Database error: {db_error}")


@router.post("/add_moto")
async def add_moto(
        new_moto: MotoWrite,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        stmt = insert(moto).values(**new_moto.model_dump())
        await session.execute(stmt)
        await session.commit()
        return {"status": 200}
    except SQLAlchemyError as db_error:
        await session.rollback()
        raise SQLAlchemyError(f"Database error: {db_error}")


@router.patch("/update_moto")
async def update_moto(
        frame_id: str,
        moto_update: MotoWrite,
        session: AsyncSession = Depends(get_async_session)
) -> dict[str, MotoBase]:
    try:
        responses = await update_model(Moto, moto_update, frame_id, session)
        return responses
    except SQLAlchemyError as db_error:
        await session.rollback()
        raise SQLAlchemyError(f"Database error: {db_error}")


@router.delete("/delete_moto")
async def delete_moto(
        frame_id: str,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        response = await delete_model(Moto, frame_id, session)
        return response
    except SQLAlchemyError as db_error:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {db_error}")


@router.get("/get_all")
async def get_all_moto(
        session: AsyncSession = Depends(get_async_session)
) -> dict[str, list[MotoBase]]:
    try:
        stmt = select(moto).order_by(moto.c.name)
        result = await session.execute(stmt)
        moto_rows = result.fetchall()
        if moto_rows:
            moto_objects = [MotoBase.model_validate(moto_object) for moto_object in moto_rows]
            return {"motos": moto_objects}
        raise HTTPException(status_code=404, detail="Moto not found")
    except SQLAlchemyError as db_error:
        await session.rollback()
        raise SQLAlchemyError(f"Database error: {db_error}")
