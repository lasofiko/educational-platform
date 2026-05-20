from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from services.ugc.auth import admin_required
from services.ugc.schemas import ModerationSchema
from services.ugc.services.ugc_svc import UGCService

moderation_bp = Blueprint('moderation', __name__, url_prefix='/api/v1/ugc')
_svc = UGCService()


@moderation_bp.post('/admin/<ugc_type>/<int:ugc_id>/moderate')
@admin_required
def moderate(ugc_type, ugc_id):
    try:
        data = ModerationSchema().load(request.get_json(silent=True) or {})
    except ValidationError as err:
        raise err
    entity = _svc.moderate(ugc_type, ugc_id, data['status'])
    return jsonify(entity), 200
