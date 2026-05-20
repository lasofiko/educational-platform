from marshmallow import Schema, fields, validate

from services.ugc.models import TARGET_TYPES


class ReviewCreateSchema(Schema):
    target_type = fields.Str(required=True, validate=validate.OneOf(TARGET_TYPES))
    target_id = fields.Int(required=True, validate=validate.Range(min=1))
    rating = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    text = fields.Str(required=True, validate=validate.Length(min=1, max=2000))
