from fastapi import APIRouter, BackgroundTasks, Depends

from src.user.base_config import current_user

from src.task.tasks import send_email_recovery_form

router = APIRouter(prefix="/recovery")


@router.get("/recovery_form/{username}")
def get_dashboard_report(username: str, background_tasks: BackgroundTasks, user=Depends(current_user)):
    send_email_recovery_form.delay(username)
    return {
        "status": 200,
        "data": "Письмо отправлено",
        "details": None
    }