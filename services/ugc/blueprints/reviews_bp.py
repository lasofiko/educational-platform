from flask import Blueprint, g, jsonify, request
from marshmallow import ValidationError

from services.ugc.auth import jwt_required
from services.ugc.schemas import ReviewCreateSchema
from services.ugc.services.ugc_svc import UGCService

reviews_bp = Blueprint('reviews', __name__, url_prefix='/api/v1/ugc')
_svc = UGCService()


@reviews_bp.post('/reviews')
@jwt_required
def create_review():
    try:
        data = ReviewCreateSchema().load(request.get_json(silent=True) or {})
    except ValidationError as err:
        raise err
    review = _svc.create_review(g.user_id, data)
    return jsonify(review.to_dict()), 201


@reviews_bp.get('/reviews')
def list_reviews():
    target_type = request.args.get('target_type')
    target_id = request.args.get('target_id', type=int)
    if not target_type or target_id is None:
        return jsonify({'error': {'code': 'validation_error', 'detail': 'target_type и target_id обязательны'}}), 400
    results = _svc.list_reviews(target_type, target_id)
    return jsonify({'results': results}), 200
