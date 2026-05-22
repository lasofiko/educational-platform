import logging
logger = logging.getLogger(__name__)
from services.ugc.common.exceptions import AlreadyReviewed, TargetNotFound, InvalidStatus
from services.ugc.services import django_client
from services.ugc.repositories import review_repo, comment_repo

def create_review(user_id: int, target_type: str, target_id: int, rating: int, text: str, review_repo):
    """Создание нового отзыва с проверкой дублей и существования цели."""
    if review_repo.exists_for_user_target(user_id,target_type,target_id):
        raise AlreadyReviewed()

    if not django_client.check_target_exists(target_type,target_id):
        raise TargetNotFound()

    logger.info("отзыв создан")
    return review_repo.create(user_id=user_id, target_type=target_type, target_id=target_id, rating=rating, text=text)

def moderate(ugc_id: int, ugc_type: str, new_status: str, moderator_id: int, review_repo, comment_repo):
    """модерация ответа/комментария"""

    valid_statuses = {'active', 'hidden', 'pending'}
    valid_types = {'review', 'comment'}

    if ugc_id not in valid_statuses:
        raise InvalidStatus()

    if ugc_type not in valid_types:
        raise InvalidStatus()

    logger.info(f"Модератор {moderator_id} меняет статус {ugc_type} с ID {ugc_id} на {new_status}")

    if ugc_type == "review":
        return review_repo.update_status(ugc_id,new_status)
    else:
        return comment_repo.update_status(ugc_id,new_status)


