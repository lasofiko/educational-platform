from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from services.notifications.db.models import Base
from services.notifications.notifications_config import get_database_url

_engine = None
_session_factory = None


def _is_sqlite_memory(url: str) -> bool:
    return url.startswith('sqlite') and ':memory:' in url


def get_engine(database_url=None):
    global _engine, _session_factory
    url = database_url or get_database_url()
    if _engine is None or str(_engine.url) != url:
        kwargs = {'echo': False}
        if _is_sqlite_memory(url):
            kwargs['connect_args'] = {'check_same_thread': False}
            kwargs['poolclass'] = StaticPool
        _engine = create_async_engine(url, **kwargs)
        _session_factory = async_sessionmaker(_engine, expire_on_commit=False)
    return _engine


def get_session_factory(database_url=None):
    get_engine(database_url)
    return _session_factory


async def init_db(database_url=None):
    engine = get_engine(database_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db_session() -> AsyncSession:
    factory = get_session_factory()
    async with factory() as session:
        yield session
