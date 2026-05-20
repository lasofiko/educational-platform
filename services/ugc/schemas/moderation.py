from marshmallow import Schema, fields, validate

from services.ugc.models import UGC_STATUSES


class ModerationSchema(Schema):
    status = fields.Str(required=True, validate=validate.OneOf(UGC_STATUSES))
