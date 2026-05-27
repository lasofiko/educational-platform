import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from services.notifications.db.session import get_engine, init_db
from services.notifications.main import create_app

TEST_DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@127.0.0.1:5434/notifications_test_db'


@pytest.fixture
def app():
    return create_app(database_url=TEST_DATABASE_URL)


@pytest_asyncio.fixture
async def client(app):
    get_engine(TEST_DATABASE_URL)
    await init_db(TEST_DATABASE_URL)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://testserver') as ac:
        yield ac
