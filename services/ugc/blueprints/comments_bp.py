from flask import Blueprint, g, jsonify, request
from marshmallow import ValidationError

from services.ugc.auth import jwt_required
from services.ugc.schemas import CommentCreateSchema
from services.ugc.services.ugc_svc import UGCService

comments_bp = Blueprint('comments', __name__, url_prefix='/api/v1/ugc')
_svc = UGCService()


@comments_bp.post('/comments')
@jwt_required
def create_comment():
    try:
        data = CommentCreateSchema().load(request.get_json(silent=True) or {})
    except ValidationError as err:
        raise err
    comment = _svc.create_comment(g.user_id, data)
    return jsonify(comment.to_dict()), 201


@comments_bp.get('/comments')
def list_comments():
    target_type = request.args.get('target_type')
    target_id = request.args.get('target_id', type=int)
    if not target_type or target_id is None:
        return jsonify({'error': {'code': 'validation_error', 'detail': 'target_type и target_id обязательны'}}), 400
    results = _svc.list_comments(target_type, target_id)
    return jsonify({'results': results}), 200
