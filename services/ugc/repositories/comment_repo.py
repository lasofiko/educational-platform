from ..models import Comment, db

class CommentRepository:
    @staticmethod
    def create(user_id, target_type, target_id, text, status='active'):
        """Создать комментарий к отзыву"""
        comment = Comment(...)
        db.session.add(comment)
        db.session.commit()
        return comment
    @staticmethod
    def list_by_target(target_id, status=None):
        """Все комментарии к отзыву"""
        query = Comment.query.filter_by(target_type='review', target_id=target_id)
        if status:
            query = query.filter_by(status=status)
        return query.order_by(Comment.created_at.desc()).all()
    @staticmethod
    def update_status(comment_id, new_status):
        """Сменить статус комментария"""
        comment = Comment.query.get(comment_id)
        if comment:
            comment.status = new_status
            db.session.commit()
        return comment