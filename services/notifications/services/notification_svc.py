from services.notifications.db.models import Notification
from services.notifications.db.session import get_session_factory
from services.notifications.schemas import NotificationCreate, NotificationOut, NotificationStatus


class NotificationService:
    async def create(self, data: NotificationCreate) -> NotificationOut:
        factory = get_session_factory()
        async with factory() as session:
            row = Notification(
                user_id=data.user_id,
                title=data.title,
                body=data.body,
                notification_type=data.notification_type,
                status=NotificationStatus.pending.value,
            )
            session.add(row)
            await session.commit()
            await session.refresh(row)
            return NotificationOut.model_validate(row)


notification_service = NotificationService()
