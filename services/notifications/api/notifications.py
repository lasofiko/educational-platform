from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.background import BackgroundTasks

from services.notifications.schemas import NodeUnlockedEvent, NotificationCreate, NotificationOut
from services.notifications.services.notification_svc import notification_service
from services.notifications.dependencies.auth import get_current_user

router = APIRouter(prefix='/notifications', tags=['notifications'])


@router.post('', response_model=NotificationOut, status_code=status.HTTP_201_CREATED)
async def create_notification(
    payload: NotificationCreate,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user),
):
    if payload.user_id != current_user["user_id"]:
        raise HTTPException(403, "Cannot create notifications for other users")
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

@router.get('/me', response_model=list[NotificationOut], status_code=status.HTTP_200_OK)
async def list_my_notifications(current_user: dict = Depends(get_current_user), limit: int = 20, offset: int = 0):
    result = await notification_service.list_for_user(current_user["user_id"], limit, offset)
    return result