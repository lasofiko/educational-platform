import os


def get_database_url():
    return os.environ.get(
        'NOTIFICATIONS_DATABASE_URL',
        'postgresql+asyncpg://postgres:postgres@127.0.0.1:5434/notifications_db',
    )
