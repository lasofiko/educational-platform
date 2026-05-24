import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from services.notifications.db.session import get_engine, init_db
from services.notifications.main import create_app

TEST_DATABASE_URL = 'sqlite+aiosqlite:///:memory:'
TEST_JWT_SECRET = 'test-secret-with-enough-entropy-32-bytes'


@pytest.fixture(autouse=True)
def jwt_secret(monkeypatch):
    monkeypatch.setenv('JWT_SECRET', TEST_JWT_SECRET)


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
