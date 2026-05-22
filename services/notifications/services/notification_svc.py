from services.notifications.db.models import Notification
from services.notifications.db.session import get_session_factory
from services.notifications.schemas import NotificationCreate, NotificationOut, NotificationStatus
from sqlalchemy import select

import asyncio

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

    async def dispatch(self, notification_id: int) -> None:
        factory = get_session_factory()
        async with factory() as session:
            row = await session.get(Notification, notification_id)
            if row is None:
                return
            await asyncio.sleep(0.1) # placeholder
            row.status = 'sent'
            await session.commit()

    async def list_for_user(self, user_id:int, limit: int, offset: int):
        factory = get_session_factory()
        async with factory() as session:
            stmt = select(Notification).where(
                Notification.user_id == user_id
            ).order_by(
                Notification.created_at.desc()
            ).limit(limit).offset(offset)

            result = await session.execute(stmt)
            rows = result.scalars().all()
            return [NotificationOut.model_validate(row) for row in rows]

            
        

notification_service = NotificationService()
