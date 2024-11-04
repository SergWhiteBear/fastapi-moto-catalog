from fastapi import APIRouter, BackgroundTasks, Depends

from src.task.tasks import send_email_recovery_form

router = APIRouter(prefix="/recovery")


@router.get("/recovery_form/{username}")
def get_dashboard_report(username: str, background_tasks: BackgroundTasks):
    send_email_recovery_form.delay(username)
    return {
        "status": 200,
        "data": "Письмо отправлено",
        "details": None
    }