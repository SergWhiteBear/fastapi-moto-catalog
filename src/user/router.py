from typing import List

from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from src.user.models import user, role
from src.database import get_async_session
from src.user.schemas import UserCreate, UserRole
from sqlalchemy.exc import SQLAlchemyError

from src.user.schemas import UserRead

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("")
async def read_users(session: AsyncSession = Depends(get_async_session)) -> dict[str, List[UserRead] | int]:
    try:
        query = select(user).order_by(user.c.username)
        result = await session.execute(query)
        users_rows = result.fetchall()
        if users_rows:
            users_info = [UserRead.model_validate(user_object) for user_object in users_rows]
            return {
                "status": 200,
                "users": users_info
            }
        raise HTTPException(status_code=404, detail="Users not found")
    except SQLAlchemyError as db_error:
        raise SQLAlchemyError(f'Database error: {db_error}')


@router.post("")
async def create_user(
        new_user: UserCreate,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        hashed_password = pwd_context.hash(new_user.password)

        user_data = {
            "email": new_user.email,
            "username": new_user.username,
            "role": new_user.role,
            "is_active": new_user.is_active,
            "is_superuser": new_user.is_superuser,
            "is_verified": new_user.is_verified,
            "hashed_password": hashed_password
        }

        stmt = insert(user).values(**user_data).returning(user.c.id)
        result = await session.execute(stmt)
        new_user_id = result.scalar_one()
        await session.commit()
        response_data = UserRead(
            id=new_user_id,
            email=new_user.email,
            username=new_user.username,
            role=new_user.role,
            is_active=new_user.is_active,
            is_superuser=new_user.is_superuser,
            is_verified=new_user.is_verified,
        )
        return {
            "status": 200,
            "user_data": response_data
        }
    except SQLAlchemyError as db_error:
        await session.rollback()
        raise SQLAlchemyError(f'Database error: {db_error}')


@router.get("/role/read")
async def read_role(session: AsyncSession = Depends(get_async_session)) -> dict[str, list[UserRole] | int]:
    try:
        query = select(role).order_by(role.c.name)
        result = await session.execute(query)
        return {
            "status": 200,
            "roles": result
        }
    except SQLAlchemyError as db_error:
        raise SQLAlchemyError(f'Database error: {db_error}')


@router.post("/role")
async def create_role(
        new_role: UserRole,
        session: AsyncSession = Depends(get_async_session)
) -> dict[str, int]:
    try:
        stmt = insert(role).values(**new_role.model_dump())
        await session.execute(stmt)
        await session.commit()
        return {"result": 200}
    except SQLAlchemyError as db_error:
        raise SQLAlchemyError(f'Database error: {db_error}')
