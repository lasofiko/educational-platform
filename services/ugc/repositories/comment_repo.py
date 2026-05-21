from services.ugc.models import Comment, db


class CommentRepository:
    def create(self, user_id, target_type, target_id, text, status='active'):
        comment = Comment(
            user_id=user_id,
            target_type=target_type,
            target_id=target_id,
            text=text,
            status=status,
        )
        db.session.add(comment)
        db.session.commit()
        return comment

    def list_visible(self, target_type, target_id):
        return (
            Comment.query.filter_by(
                target_type=target_type,
                target_id=target_id,
            )
            .filter(Comment.status != 'hidden')
            .order_by(Comment.created_at.desc())
            .all()
        )

    def get_by_id(self, comment_id):
        return db.session.get(Comment, comment_id)

    def set_status(self, comment_id, status):
        comment = self.get_by_id(comment_id)
        if comment is None:
            return None
        comment.status = status
        db.session.commit()
        return comment
