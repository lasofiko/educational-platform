from services.ugc.models import UGC_TYPES
from services.ugc.common.exceptions import UGCNotFoundError
from services.ugc.repositories import ReviewRepository, CommentRepository
from services.ugc.services.django_client import DjangoClient


class UGCService:
    def __init__(
        self,
        review_repo=None,
        comment_repo=None,
        django_client=None,
    ):
        self.review_repo = review_repo or ReviewRepository()
        self.comment_repo = comment_repo or CommentRepository()
        self.django_client = django_client or DjangoClient()

    def create_review(self, user_id, data):
        self.django_client.check_target_exists(data['target_type'], data['target_id'])
        return self.review_repo.create(
            user_id=user_id,
            target_type=data['target_type'],
            target_id=data['target_id'],
            rating=data['rating'],
            text=data['text'],
        )

    def list_reviews(self, target_type, target_id):
        reviews = self.review_repo.list_visible(target_type, target_id)
        return [review.to_dict() for review in reviews]

    def create_comment(self, user_id, data):
        self.django_client.check_target_exists(data['target_type'], data['target_id'])
        comment = self.comment_repo.create(
            user_id=user_id,
            target_type=data['target_type'],
            target_id=data['target_id'],
            text=data['text'],
        )
        return comment

    def list_comments(self, target_type, target_id):
        comments = self.comment_repo.list_visible(target_type, target_id)
        return [comment.to_dict() for comment in comments]

    def moderate(self, ugc_type, ugc_id, status):
        if ugc_type not in UGC_TYPES:
            raise UGCNotFoundError(message=f'Неизвестный тип UGC: {ugc_type}')

        if ugc_type == 'review':
            entity = self.review_repo.set_status(ugc_id, status)
        else:
            entity = self.comment_repo.set_status(ugc_id, status)

        if entity is None:
            raise UGCNotFoundError()
        return entity.to_dict()
