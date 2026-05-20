import os


def get_database_url():
    return os.environ.get(
        'NOTIFICATIONS_DATABASE_URL',
        'sqlite+aiosqlite:///:memory:',
    )
