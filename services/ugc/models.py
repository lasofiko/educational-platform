from flask_sqlalchemy import SQLAlchemy
from enum import Enum

db = SQLAlchemy()

class TargetType(str, Enum):
    LESSON = 'lesson'
    SUBJECT = 'subject'
    REVIEW = 'review'
class StatusType(str, Enum):
    ACTIVE = 'active'
    HIDDEN = 'hidden'
    PENDING = 'pending'
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    target_type = db.Column(db.String(20), nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(2000))
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    __table_args__ = (db.UniqueConstraint('user_id', 'target_type', 'target_id', name='unique_user_target'))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'target_type': self.target_type,
            'target_id': self.target_id,
            'rating': self.rating,
            'text': self.text,
            'status': self.status,
        }

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    target_type = db.Column(db.String(20), nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(2000), nullable=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'target_type': self.target_type,
            'target_id': self.target_id,
            'text': self.text,
            'status': self.status,
        }

TARGET_TYPES = ('lesson', 'subject')
UGC_TYPES = ('review', 'comment')
UGC_STATUSES = ('active', 'hidden', 'pending')