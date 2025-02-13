from src.dao.base import BaseDAO
from src.order.models import Basket, Order, OrderItem
from src.dao.database import BasketMoto


class BasketDAO(BaseDAO):
    model = Basket


class BasketMotoDAO(BaseDAO):
    model = BasketMoto


class OrderDAO(BaseDAO):
    model = Order

class OrderItemDAO(BaseDAO):
    model = OrderItem
