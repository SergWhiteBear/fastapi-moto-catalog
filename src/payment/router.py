import time

from celery.result import AsyncResult
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.session_maker import TransactionSessionDep
from src.dao.sql_enums import OrderEnum, PaymentTypeEnum
from src.payment.dao import PaymentDao
from src.payment.schemas import SPaymentCreate, SPayment
from src.config import celery_app

router = APIRouter(prefix='/payment', tags=['Payment'])


@router.post('/create_payment')
async def create_payment(payment: SPayment, session: AsyncSession = TransactionSessionDep):
    task = celery_app.send_task("task.create_payment", args=[payment.id])
    status = await get_payment_status(task.id)
    if status["detail"]["status"] == "success":
        await PaymentDao.add(session, values=SPaymentCreate(id=payment.id,
                                                            order_id=payment.order_id,
                                                            status=PaymentTypeEnum.success))
        celery_app.send_task("task.update_order_status", args=[payment.order_id, OrderEnum.paid])
        return status
    elif status["detail"]["status"] == "failed":
        await PaymentDao.add(session, values=SPaymentCreate(id=payment.id,
                                                            order_id=payment.order_id,
                                                            status=PaymentTypeEnum.failure))
        celery_app.send_task("task.update_order_status", args=[payment.order_id, OrderEnum.canceled])
        return status
    return status["detail"]["status"]


@router.get('/{task_id}/status')
async def get_payment_status(task_id: str) -> dict:
    task = AsyncResult(task_id)

    if task.state == "PENDING":
        return {"status": "Processing...", "detail": "None"}
    elif task.state == "SUCCESS":
        return {"status": "Success", "detail": task.result}
    else:
        return {"status": "Failed", "detail": task.result}
