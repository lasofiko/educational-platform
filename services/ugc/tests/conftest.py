import jwt
import pytest

from services.ugc.app import create_test_app
from services.ugc.models import db

TEST_JWT_SECRET = 'test-jwt-secret'
DJANGO_TEST_BASE = 'http://django.test'


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setenv('JWT_SECRET', TEST_JWT_SECRET)
    monkeypatch.setenv('DJANGO_BASE_URL', DJANGO_TEST_BASE)
    application = create_test_app()
    application.config['JWT_SECRET'] = TEST_JWT_SECRET
    application.config['DJANGO_BASE_URL'] = DJANGO_TEST_BASE

    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def make_token(user_id=1, is_staff=False):
    return jwt.encode(
        {'user_id': user_id, 'is_staff': is_staff},
        TEST_JWT_SECRET,
        algorithm='HS256',
    )


@pytest.fixture
def auth_headers():
    def _headers(user_id=1, is_staff=False):
        token = make_token(user_id=user_id, is_staff=is_staff)
        if isinstance(token, bytes):
            token = token.decode()
        return {'Authorization': f'Bearer {token}'}
    return _headers


@pytest.fixture
def django_exists_url():
    def _builder(target_type, target_id):
        return f'{DJANGO_TEST_BASE}/api/v1/courses/objects/{target_type}/{target_id}/exists/'
    return _builder