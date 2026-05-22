from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class NotificationStatus(str, Enum):
    pending = 'pending'
    sent = 'sent'
    failed = 'failed'


class NotificationCreate(BaseModel):
    user_id: int = Field(ge=1)
    title: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1, max_length=2000)
    notification_type: str = Field(default='info', min_length=1, max_length=50)


class NotificationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str
    body: str
    notification_type: str
    status: NotificationStatus
    created_at: datetime

class NodeUnlockedEvent(BaseModel):
    user_id: int = Field(ge=1)
    node_id: int = Field(ge=1)
    node_title: str = Field(min_length=1, max_length=200)