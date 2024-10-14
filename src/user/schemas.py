from typing import Optional

from fastapi_users import schemas

from pydantic import UUID4, BaseModel, EmailStr, Field


class UserRead(schemas.BaseUser[int]):
    id: UUID4
    email: EmailStr
    username: str
    role: str
    is_active: bool = Field(default=True, description="Активен ли пользователь")
    is_superuser: bool = Field(default=False, description="Является ли суперпользователем")
    is_verified: bool = Field(default=False, description="Подтвержден ли пользователь")

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str
    role: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    class Config:
        from_attributes = True


class Permission(BaseModel):
    is_superuser: bool = False
    is_active: bool = True
    is_verified: bool = False


class UserRole(BaseModel):
    name: str
    permissions: Permission

    class Config:
        from_attributes = True
