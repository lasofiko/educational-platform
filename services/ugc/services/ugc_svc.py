from services.ugc.common.exceptions import AlreadyReviewed, UGCNotFound
from services.ugc.models import UGC_TYPES
from services.ugc.repositories import CommentRepository, ReviewRepository
from services.ugc.services.django_client import DjangoClient


class UGCService:
    def __init__(self, review_repo=None, comment_repo=None, django_client=None):
        self.review_repo = review_repo or ReviewRepository()
        self.comment_repo = comment_repo or CommentRepository()
        self.django_client = django_client or DjangoClient()

    def create_review(self, user_id, data):
        self.django_client.check_target_exists(data['target_type'], data['target_id'])
        if self.review_repo.exists_for_user_target(
            user_id, data['target_type'], data['target_id'],
        ):
            raise AlreadyReviewed(user_id, data['target_type'], data['target_id'])
        return self.review_repo.create(
            user_id=user_id,
            target_type=data['target_type'],
            target_id=data['target_id'],
            rating=data['rating'],
            text=data.get('text'),
        )

    def list_reviews(self, target_type, target_id):
        rows = self.review_repo.list_by_target(target_type, target_id)
        visible = [r for r in rows if r.status == 'active']
        return [r.to_dict() for r in visible]

    def create_comment(self, user_id, data):
        self.django_client.check_target_exists(data['target_type'], data['target_id'])
        return self.comment_repo.create(
            user_id=user_id,
            target_type=data['target_type'],
            target_id=data['target_id'],
            text=data['text'],
        )

    def list_comments(self, target_type, target_id):
        rows = self.comment_repo.list_by_target(target_type, target_id)
        visible = [c for c in rows if c.status == 'active']
        return [c.to_dict() for c in visible]

    def moderate(self, ugc_type, ugc_id, status):
        if ugc_type not in UGC_TYPES:
            raise UGCNotFound(ugc_type, ugc_id)

        if ugc_type == 'review':
            entity = self.review_repo.update_status(ugc_id, status)
        else:
            entity = self.comment_repo.update_status(ugc_id, status)

        if entity is None:
            raise UGCNotFound(ugc_type, ugc_id)
        return entity.to_dict()