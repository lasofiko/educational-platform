from fastapi import APIRouter, status

from services.notifications.schemas import NotificationCreate, NotificationOut
from services.notifications.services.notification_svc import notification_service

router = APIRouter(prefix='/notifications', tags=['notifications'])


@router.post('', response_model=NotificationOut, status_code=status.HTTP_201_CREATED)
async def create_notification(payload: NotificationCreate):
    return await notification_service.create(payload)
