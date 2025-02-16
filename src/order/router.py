import uuid
from typing import Optional

from fastapi import APIRouter, Response, Depends, Request

from src.dao.sql_enums import OrderEnum
from src.exceptions import *
from src.auth.dependencies import get_current_user
from src.moto.dao import MotoDAO
from src.order.schemas import BasketModel, BasketMotoModel, BasketReadModel, OrderModel, OrderMotoModel, OrderFilter
from src.order.dao import BasketDAO, BasketMotoDAO, OrderDAO, OrderItemDAO
from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.session_maker import TransactionSessionDep, SessionDep
from src.utils.serialization import serialize_objects
from src.user.models import User
from src.config import celery_app

router = APIRouter(prefix='/basket', tags=['Basket'])


def get_guest_id(request: Request, response: Response):
    guest_id = request.cookies.get("guest_id")
    if not guest_id:
        guest_id = str(uuid.uuid4())
        response.set_cookie(key="guest_id", value=guest_id, httponly=True, max_age=60 * 60)
    return guest_id


@router.get('/')
async def get_basket(filters: BasketModel = Depends(), session: AsyncSession = SessionDep):
    basket = await BasketDAO.find_one_or_none(session, filters=filters)
    if not basket:
        raise BasketNotFoundException
    return basket


@router.post('/add_moto')
async def add_moto_basket(request: Request, response: Response, moto_id: int,
                          user: Optional[User] = Depends(get_current_user),
                          session: AsyncSession = TransactionSessionDep):
    guest_id = None
    try:
        if user:
            basket = await BasketDAO.find_one_or_none_by_id(session=session, data_id=user.id)
        else:
            guest_id = get_guest_id(request, response)
            basket = await BasketDAO.find_one_or_none(session=session, filters=BasketModel(guest_id=guest_id))

        if basket is None:
            basket = await BasketDAO.add(session=session,
                                         values=BasketModel(user_id=(user.id if user else None), guest_id=guest_id))

        moto = await MotoDAO.find_one_or_none_by_id(session=session, data_id=moto_id)
        if moto is None:
            raise MotoNotFoundException

        # Проверка, есть ли уже мотоцикл в корзине
        existing_item = await BasketMotoDAO.find_one_or_none(session=session,
                                                             filters=BasketMotoModel(id=basket.id, moto_id=moto_id))
        if existing_item:
            raise ItemAlreadyExistsException

        new_row = await BasketMotoDAO.add(session=session, values=BasketMotoModel(id=basket.id, moto_id=moto_id))
        return {"detail": "Мотоцикл добавлен в корзину", "new_row": new_row}

    except HTTPException:
        raise
    except Exception as e:
        raise InternalServerErrorException


@router.get('/get_with_relation/')
async def get_basket_with_relation(filters: BasketMotoModel = Depends(),
                                   session: AsyncSession = SessionDep):
    basket = await BasketMotoDAO.get_with_relationships(
        session=session,
        filters=filters,
        relationships=["basket", "moto", "moto.engine"]
    )
    if basket is None:
        raise BasketNotFoundException
    return serialize_objects(basket, BasketReadModel, exclude_fields=[])


@router.post('/create_order')
async def create_order(user: User = Depends(get_current_user),
                       session: AsyncSession = TransactionSessionDep):
    if not user:
        raise ForbiddenException
    user_basket = await BasketDAO.find_one_or_none(session=session, filters=BasketModel(user_id=user.id))
    if not user_basket:
        raise BasketNotFoundException
    rows_user_basket = await BasketMotoDAO.get_with_relationships(session=session,
                                                                  filters=BasketMotoModel(id=user_basket.id),
                                                                  relationships=["moto"])
    if not rows_user_basket:
        raise BasketEmptyException
    total_price = 0
    items = []
    try:
        order = await OrderDAO.add(session=session,
                                   values=OrderModel(user_id=user_basket.user_id, total_price=total_price))
        for basket_moto in rows_user_basket:
            order_moto = await OrderItemDAO.add(session=session,
                                                values=OrderMotoModel(order_id=order.id, moto_id=basket_moto.moto.id))
            total_price += basket_moto.moto.price
            items.append(order_moto)

        await OrderDAO.update(session=session, filters=OrderFilter(user_id=user_basket.user_id),
                              values=OrderModel(total_price=total_price))
        await BasketDAO.delete(session=session, filters=BasketModel(user_id=user_basket.user_id))

        # перед этим идет логика с платежами или она скорее всего была сделана до создания заказа
        celery_app.send_task("task.update_order_status", args=[order.id, OrderEnum.paid])
        return {"detail": "Заказ успешно создан", "order_id": order.id, "total_price": total_price}
    except Exception as e:
        raise InternalServerErrorException


@router.post('/orders/{order_id}/{status_}')
async def update_order_status(order_id: int, status_: OrderEnum, session: AsyncSession = TransactionSessionDep):
    order = await OrderDAO.find_one_or_none_by_id(session=session, data_id=order_id)
    if order is None:
        return {"detail": "Не найден заказ"}
    old_status = order.status
    order_data = OrderModel.model_validate(order, from_attributes=True)
    updated_order = order_data.model_copy(update={"status": status_})
    await OrderDAO.update(session=session, filters=OrderFilter(id=order_id), values=updated_order.model_dump())
    return {"detail": "Статус изменен", "order_id": order_id, "status": updated_order.status, "old_status": old_status}
