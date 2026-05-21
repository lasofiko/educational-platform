from fastapi import APIRouter, status
from fastapi.background import BackgroundTasks

from services.notifications.schemas import NodeUnlockedEvent, NotificationCreate, NotificationOut
from services.notifications.services.notification_svc import notification_service

router = APIRouter(prefix='/notifications', tags=['notifications'])


@router.post('', response_model=NotificationOut, status_code=status.HTTP_201_CREATED)
async def create_notification(payload: NotificationCreate, background_tasks: BackgroundTasks):
    result = await notification_service.create(payload)
    background_tasks.add_task(notification_service.dispatch, result.id)
    return result

@router.post('/node-unlocked', response_model=NotificationOut, status_code=status.HTTP_201_CREATED)
async def handle_node_unlocked(payload: NodeUnlockedEvent, background_tasks: BackgroundTasks):
    notification = NotificationCreate(
        user_id = payload.user_id, 
        title = "Тема разблокирована",
        body = f"Вы открыли тему: «{payload.node_title}»",
        notification_type = "node_unlocked"
        )
    result = await notification_service.create(notification)
    background_tasks.add_task(notification_service.dispatch, result.id)
    
    return result

