from marshmallow import Schema, fields, validate

from services.ugc.models import TARGET_TYPES


class CommentCreateSchema(Schema):
    target_type = fields.Str(required=True, validate=validate.OneOf(TARGET_TYPES))
    target_id = fields.Int(required=True, validate=validate.Range(min=1))
    text = fields.Str(required=True, validate=validate.Length(min=1, max=2000))
