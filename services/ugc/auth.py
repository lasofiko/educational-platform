from functools import wraps

import jwt
from flask import current_app, g, request

from services.ugc.common.exceptions import ForbiddenError, UnauthorizedError


def _decode_token():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        raise UnauthorizedError(message='Требуется заголовок Authorization: Bearer')
    token = auth_header[7:].strip()
    if not token:
        raise UnauthorizedError(message='Пустой токен')
    try:
        return jwt.decode(
            token,
            current_app.config['JWT_SECRET'],
            algorithms=['HS256'],
        )
    except jwt.PyJWTError as exc:
        raise UnauthorizedError(message='Недействительный токен') from exc


def jwt_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        payload = _decode_token()
        user_id = payload.get('user_id')
        if user_id is None:
            raise UnauthorizedError(message='В токене нет user_id')
        g.user_id = int(user_id)
        g.is_staff = bool(payload.get('is_staff', False))
        return view(*args, **kwargs)

    return wrapper


def admin_required(view):
    @wraps(view)
    @jwt_required
    def wrapper(*args, **kwargs):
        if not g.is_staff:
            raise ForbiddenError(message='Только для администраторов')
        return view(*args, **kwargs)

    return wrapper
