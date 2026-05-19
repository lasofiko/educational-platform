from sqlalchemy.exc import IntegrityError

from services.ugc.models import Review, db
from services.ugc.common.exceptions import DuplicateReviewError


class ReviewRepository:
    def create(self, user_id, target_type, target_id, rating, text, status='active'):
        review = Review(
            user_id=user_id,
            target_type=target_type,
            target_id=target_id,
            rating=rating,
            text=text,
            status=status,
        )
        db.session.add(review)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise DuplicateReviewError()
        return review

    def list_visible(self, target_type, target_id):
        return (
            Review.query.filter_by(
                target_type=target_type,
                target_id=target_id,
            )
            .filter(Review.status != 'hidden')
            .order_by(Review.created_at.desc())
            .all()
        )

    def get_by_id(self, review_id):
        return db.session.get(Review, review_id)

    def set_status(self, review_id, status):
        review = self.get_by_id(review_id)
        if review is None:
            return None
        review.status = status
        db.session.commit()
        return review
