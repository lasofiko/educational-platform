from ..models import Review, db

class ReviewRepository:
    @staticmethod
    def create(user_id, target_type, target_id, rating, text, status='active'):
        review = Review(
            user_id=user_id,
            target_type=target_type,
            target_id=target_id,
            rating=rating,
            text=text,
            status=status,
        )
        db.session.add(review)
        db.session.commit()
        return review
    @staticmethod
    def get_by_id(review_id):
        """Найти отзыв по ID"""
        return Review.query.get(review_id)
    @staticmethod
    def list_by_target(target_type, target_id, status=None):
        """Все отзывы на урок/предмет"""
        query = Review.query.filter_by(target_type=target_type, target_id=target_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(Review.created_at.desc()).all()
    @staticmethod
    def exists_for_user_target(user_id, target_type, target_id):
        """Для запрета дублей"""
        return Review.query.filter_by(user_id=user_id, target_type=target_type, target_id=target_id).first() is not None
    @staticmethod
    def update_status(review_id, new_status):
        """Сменить статус (активный/скрытый/на модерации)"""
        review = Review.query.get(review_id)
        if review:
            review.status = new_status
            db.session.commit()
        return review