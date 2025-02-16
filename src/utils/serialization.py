from pydantic import BaseModel
from typing import List, Type, Any


def serialize_objects(
        objects: List[Any],
        schema: Type[BaseModel],
        exclude_fields: List[str] = None
):
    """
    Универсальная функция для сериализации SQLAlchemy-объектов с Pydantic,
    позволяющая скрывать определённые поля.
    """
    return [
        schema.model_validate(obj, from_attributes=True).model_dump(exclude=set(exclude_fields))
        for obj in objects
    ]