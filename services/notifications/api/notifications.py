from fastapi import APIRouter, status

from services.notifications.schemas import NodeUnlockedEvent, NotificationCreate, NotificationOut
from services.notifications.services.notification_svc import notification_service

router = APIRouter(prefix='/notifications', tags=['notifications'])


@router.post('', response_model=NotificationOut, status_code=status.HTTP_201_CREATED)
async def create_notification(payload: NotificationCreate):
    return await notification_service.create(payload)

@router.post('/node-unlocked', response_model=NotificationOut, status_code=status.HTTP_201_CREATED)
async def handle_node_unlocked(payload: NodeUnlockedEvent):
    notification = NotificationCreate(
        user_id = payload.user_id, 
        title = "Тема разблокирована",
        body = f"Вы открыли тему: «{payload.node_title}»",
        notification_type = "node_unlocked"
        )

    return await notification_service.create(notification)
