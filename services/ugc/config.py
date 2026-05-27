import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'UGC_DATABASE_URL',
        'postgresql+psycopg2://postgres:postgres@127.0.0.1:5432/ugc_db',
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET = os.environ.get('JWT_SECRET', 'change-me-same-as-django-secret-for-dev')
    DJANGO_BASE_URL = os.environ.get('DJANGO_BASE_URL', 'http://localhost:8000').rstrip('/')


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@127.0.0.1:5433/ugc_db'
