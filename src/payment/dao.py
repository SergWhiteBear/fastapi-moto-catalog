from src.dao.base import BaseDAO
from src.payment.models import Payment


class PaymentDao(BaseDAO):
    model = Payment
