from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from typing import List
from src.database import get_async_session
from fastapi import APIRouter, Depends
from src.moto.models import moto, engine
from src.moto.schemas import MotoSchema, EngineSchema
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(
    prefix="/moto",
    tags=["moto"],
)


@router.get("/get_engine")
async def get_engine(
        engine_name: str,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(engine).where(engine.c.engine_name == engine_name)
        result = await session.execute(query)
        engine_data = result.fetchone()
        return {"result": engine_data._asdict()}
    except SQLAlchemyError as db_error:
        await session.rollback()
        return {"status": "failed", "reason": f"Database error: {str(db_error)}"}
    except Exception as e:
        await session.rollback()
        return {"status": "failed", "reason": f"Unexpected error: {str(e)}"}


@router.get("/get_moto/{id_moto}")
async def get_moto(
        id_moto: int,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(moto).where(moto.c.id == id_moto)
        result = await session.execute(query)
        moto_data = result.fetchone()
        return {"moto": moto_data._asdict()}
    except SQLAlchemyError as db_error:
        await session.rollback()
        return {"status": "failed", "reason": f"Database error: {str(db_error)}"}
    except Exception as e:
        await session.rollback()
        return {"status": "failed", "reason": f"Unexpected error: {str(e)}"}


@router.post("/add_engine")
async def add_engine(
        new_engine: EngineSchema,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        stmt = insert(engine).values(**new_engine.dict()).returning(engine.c.engine_name)
        await session.execute(stmt)
        await session.commit()
        return {"result": "success"}
    except SQLAlchemyError as db_error:
        await session.rollback()
        return {"status": "failed", "reason": f"Database error: {str(db_error)}"}
    except Exception as e:
        await session.rollback()
        return {"status": "failed", "reason": f"Unexpected error: {str(e)}"}


@router.post("/add_moto")
async def add_moto(
        new_moto: MotoSchema,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        stmt = insert(moto).values(**new_moto.dict()).returning(moto.c.id)
        await session.execute(stmt)
        await session.commit()
        return {"status": "success"}
    except SQLAlchemyError as db_error:
        await session.rollback()
        return {"status": "failed", "reason": f"Database error: {str(db_error)}"}
    except Exception as e:
        await session.rollback()
        return {"status": "failed", "reason": f"Unexpected error: {str(e)}"}

@router.get("/get_all", response_model=List[MotoSchema])
async def get_all_moto(
        session: AsyncSession = Depends(get_async_session)
):
    try:
        stmt = select(moto).order_by(moto.c.id)
        motos = await session.execute(stmt)
        return motos
    except SQLAlchemyError as db_error:
        await session.rollback()
        return {"status": "failed", "reason": f"Database error: {str(db_error)}"}
    except Exception as e:
        await session.rollback()
        return {"status": "failed", "reason": f"Unexpected error: {str(e)}"}
