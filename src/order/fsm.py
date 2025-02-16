from src.dao.sql_enums import OrderEnum


class OrderFSM:
    """FSM (машина состояний) для заказов"""

    ALLOWED_TRANSITIONS = {
        OrderEnum.pending: [OrderEnum.paid, OrderEnum.canceled, OrderEnum.awaiting_payment],
        OrderEnum.paid: [OrderEnum.processing, OrderEnum.failed, OrderEnum.canceled],
        OrderEnum.processing: [OrderEnum.shipped, OrderEnum.failed, OrderEnum.canceled],
        OrderEnum.shipped: [OrderEnum.delivered, OrderEnum.failed, OrderEnum.partial_shipped],
        OrderEnum.delivered: [OrderEnum.completed, OrderEnum.failed],
        OrderEnum.completed: [],
        OrderEnum.canceled: [],
        OrderEnum.failed: [],
        OrderEnum.on_hold: [OrderEnum.processing, OrderEnum.canceled],
        OrderEnum.awaiting_payment: [OrderEnum.paid, OrderEnum.canceled],
        OrderEnum.backordered: [OrderEnum.shipped, OrderEnum.failed, OrderEnum.canceled],
        OrderEnum.partial_shipped: [OrderEnum.shipped, OrderEnum.failed, OrderEnum.canceled],
    }

    @staticmethod
    def can_transition(current_status: OrderEnum, new_status: OrderEnum) -> bool:
        """Проверяем, можно ли сменить статус"""
        return new_status in OrderFSM.ALLOWED_TRANSITIONS.get(current_status, [])