from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from src.database import get_async_session
from fastapi import APIRouter, Depends, HTTPException
from src.moto.models import moto, engine, Engine
from src.moto.schemas import MotoBase, EngineBase, EngineWrite, MotoWrite
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(
    prefix="/moto",
    tags=["moto"],
)


@router.get("/get_engine")
async def get_engine(
        engine_id: str,
        session: AsyncSession = Depends(get_async_session)
) -> dict[str, EngineBase]:
    try:
        query = select(engine).where(engine.c.engine_id == engine_id)
        result = await session.execute(query)
        await session.commit()
        engine_data = result.fetchone()
        if engine_data:
            return {f"{engine_id}": EngineBase.model_validate(engine_data)}
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


@router.patch("/update_engine")
async def update_engine(
        engine_id: str,
        engine_update: EngineBase,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        stmt = (
            update(engine).
            where(engine.c.engine_id == engine_id).
            values(engine_update.model_dump(exclude_unset=True))
        )
        result = await session.execute(stmt)

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Not Found")

        await session.commit()
        return {"updated_engine": 200 }
    except SQLAlchemyError as db_error:
        await session.rollback()
        raise SQLAlchemyError(f"Database error: {db_error}")


@router.delete("/delete_engine")
async def delete_engine(
        engine_id: str,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        stmt = delete(engine).where(engine.c.engine_id == engine_id)
        result = await session.execute(stmt)
        await session.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Not Found")
        return {"status": 200, "msg": "Deleted Successfully"}
    except SQLAlchemyError as db_error:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {db_error}")


@router.get("/get_moto")
async def get_moto(
        frame_id: str,
        session: AsyncSession = Depends(get_async_session)
) -> dict[str, list[MotoBase]]:
    try:
        query = select(moto).where(moto.c.frame_id == frame_id)
        result = await session.execute(query)
        moto_rows = result.fetchall()
        if moto_rows:
            moto_objects = [MotoBase.model_validate(moto_object) for moto_object in moto_rows]
            return {"moto": moto_objects}
        raise HTTPException(status_code=404, detail="Moto not found")
    except SQLAlchemyError as db_error:
        await session.rollback()
        raise SQLAlchemyError(f"Database error: {db_error}")


@router.post("/add_moto", response_model=MotoWrite)
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
        moto_update: MotoBase,
        session: AsyncSession = Depends(get_async_session)
) -> dict[str, MotoBase]:
    try:
        query = (
            select(moto).
            where(moto.c.frame_id == frame_id)
        )
        result = await session.execute(query)
        existing_moto = result.scalars().first()
        if not existing_moto:
            raise HTTPException(status_code=404, detail="Moto not found")

        for key, value in moto_update.model_dump(exclude_unset=True).items():
            setattr(existing_moto, key, value)

        await session.commit()
        await session.refresh(existing_moto)

        return {"updated_moto": MotoBase.model_validate(existing_moto)}
    except SQLAlchemyError as db_error:
        await session.rollback()
        raise SQLAlchemyError(f"Database error: {db_error}")


@router.delete("/delete_moto")
async def delete_moto(
        frame_id: str,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        stmt = delete(moto).where(moto.c.frame_id == frame_id)
        result = await session.execute(stmt)
        await session.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Not Found")
        return {"status": 200, "msg": "Deleted Successfully"}
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