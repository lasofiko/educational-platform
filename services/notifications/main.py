from contextlib import asynccontextmanager

from fastapi import FastAPI

from services.notifications.api.health import router as health_router
from services.notifications.api.notifications import router as notifications_router
from services.notifications.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    database_url = getattr(app.state, 'database_url', None)
    await init_db(database_url)
    yield


def create_app(database_url=None) -> FastAPI:
    app = FastAPI(
        title='Notifications API',
        version='1.0.0',
        lifespan=lifespan,
    )
    if database_url is not None:
        app.state.database_url = database_url

    app.include_router(health_router)
    app.include_router(notifications_router, prefix='/api/v1')
    return app


app = create_app()
