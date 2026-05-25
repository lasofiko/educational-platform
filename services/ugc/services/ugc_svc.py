import logging

from services.ugc.common.exceptions import (
    AlreadyReviewed,
    InvalidStatus,
    TargetNotFound,
    UGCNotFound,
)
from services.ugc.models import UGC_TYPES
from services.ugc.repositories import CommentRepository, ReviewRepository
from services.ugc.services import django_client
from services.ugc.services.django_client import DjangoClient

logger = logging.getLogger(__name__)


def create_review(
    user_id: int,
    target_type: str,
    target_id: int,
    rating: int,
    text: str,
    review_repo,
):
    """Создание нового отзыва с проверкой дублей и существования цели."""
    if review_repo.exists_for_user_target(user_id, target_type, target_id):
        raise AlreadyReviewed(user_id, target_type, target_id)

    if not django_client.check_target_exists(target_type, target_id):
        raise TargetNotFound(target_type, target_id)

    logger.info("отзыв создан")
    return review_repo.create(
        user_id=user_id,
        target_type=target_type,
        target_id=target_id,
        rating=rating,
        text=text,
    )


def moderate(
    ugc_id: int,
    ugc_type: str,
    new_status: str,
    moderator_id: int,
    review_repo,
    comment_repo,

):
    """Модерация отзыва/комментария."""
    valid_statuses = {"active", "hidden", "pending"}
    valid_types = {"review", "comment"}

    if new_status not in valid_statuses:
        raise InvalidStatus(new_status)

    if ugc_type not in valid_types:
        raise InvalidStatus(ugc_type)

    logger.info(
        "Модератор %s меняет статус %s с ID %s на %s",
        moderator_id,
        ugc_type,
        ugc_id,
        new_status,
    )

    if ugc_type == "review":
        return review_repo.update_status(ugc_id, new_status)
    return comment_repo.update_status(ugc_id, new_status)

class UGCService:
    def __init__(self, review_repo=None, comment_repo=None, django_client=None):
        self.review_repo = review_repo or ReviewRepository()
        self.comment_repo = comment_repo or CommentRepository()
        self.django_client = django_client or DjangoClient()

    def create_review(self, user_id, data):
        return create_review(
            user_id,
            data["target_type"],
            data["target_id"],
            data["rating"],
            data.get("text"),
            self.review_repo,
        )

    def list_reviews(self, target_type, target_id):
        rows = self.review_repo.list_by_target(target_type, target_id)
        visible = [r for r in rows if r.status == "active"]
        return [r.to_dict() for r in visible]

    def create_comment(self, user_id, data):
        self.django_client.check_target_exists(data["target_type"], data["target_id"])
        return self.comment_repo.create(
            user_id=user_id,
            target_type=data["target_type"],
            target_id=data["target_id"],
            text=data["text"],
        )

    def list_comments(self, target_type, target_id):
        rows = self.comment_repo.list_by_target(target_type, target_id)
        visible = [c for c in rows if c.status == "active"]
        return [c.to_dict() for c in visible]

    def moderate(self, ugc_type, ugc_id, status):
        if ugc_type not in UGC_TYPES:
            raise UGCNotFound(ugc_type, ugc_id)

        entity = moderate(
            ugc_id,
            ugc_type,
            status,
            moderator_id=0,
            review_repo=self.review_repo,
            comment_repo=self.comment_repo,
        )
        if entity is None:
            raise UGCNotFound(ugc_type, ugc_id)
        return entity.to_dict()