import uuid
from itertools import accumulate
from typing import Optional

from fastapi import APIRouter, Response, Depends, HTTPException, Request

from src.auth.dependencies import get_current_user
from src.moto.dao import MotoDAO
from src.order.schemas import BasketModel, BasketMotoModel, BasketReadModel, OrderModel, OrderMotoModel, OrderFilter
from src.order.dao import BasketDAO, BasketMotoDAO, OrderDAO, OrderItemDAO
from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.session_maker import TransactionSessionDep, SessionDep
from src.utils.serialization import serialize_objects
from src.user.models import User

router = APIRouter(prefix='/basket', tags=['Basket'])


def get_guest_id(request: Request, response: Response):
    guest_id = request.cookies.get("guest_id")
    if not guest_id:
        guest_id = str(uuid.uuid4())
        response.set_cookie(key="guest_id", value=guest_id, httponly=True, max_age=60 * 60)
    return guest_id


@router.get('/')
async def get_basket(filters: BasketModel = Depends(), session: AsyncSession = TransactionSessionDep):
    basket = await BasketDAO.find_one_or_none(session, filters=filters)
    if basket:
        return basket
    return {"None"}


@router.post('/add_moto')
async def add_moto_basket(request: Request, response: Response, moto_id: int,
                          user: Optional[User] = Depends(get_current_user),
                          session: AsyncSession = TransactionSessionDep):
    guest_id = None
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
        return HTTPException(status_code=404, detail='Moto not found')
    new_row = await BasketMotoDAO.add(session=session, values=BasketMotoModel(id=basket.id, moto_id=moto_id))
    return new_row


@router.get('/get_with_relation/')
async def get_basket_with_relation(filters: BasketMotoModel = Depends(), session: AsyncSession = TransactionSessionDep):
    basket = await BasketMotoDAO.get_with_relationships(
        session=session,
        filters=filters,
        relationships=["basket", "moto", "moto.engine"]
    )
    if basket is None:
        return HTTPException(status_code=404, detail='Basket not found')
    return serialize_objects(basket, BasketReadModel, exclude_fields=[])

#TODO: Оформление дописать везде
@router.post('/create_order')
async def create_order(request: Request, response: Response, user: int,
                       session: AsyncSession = TransactionSessionDep):
    user_basket = await BasketDAO.find_one_or_none(session=session, filters=BasketModel(user_id=user))
    if not user_basket:
        raise HTTPException(status_code=404, detail="Basket not found")
    rows_user_basket = await BasketMotoDAO.get_with_relationships(session=session,
                                                                  filters=BasketMotoModel(id=user_basket.id),
                                                                  relationships=["moto"])
    total_price = 0
    items = []
    order = await OrderDAO.add(session=session, values=OrderModel(user_id=user_basket.user_id, total_price=total_price))
    for basket_moto in rows_user_basket:
        order_moto = await OrderItemDAO.add(session=session,
                                            values=OrderMotoModel(order_id=order.id, moto_id=basket_moto.moto.id))
        total_price += basket_moto.moto.price
        items.append(order_moto)

    await OrderDAO.update(session=session, filters=OrderFilter(user_id=user_basket.user_id),
                          values=OrderModel(total_price=total_price))
    await BasketDAO.delete(session=session, filters=BasketModel(user_id=user_basket.user_id))
    return items
