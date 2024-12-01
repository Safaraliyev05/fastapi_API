from contextlib import asynccontextmanager

from fastapi import FastAPI

from models import db
from routers import shop_router, category_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.create_all()
    app.include_router(shop_router)
    app.include_router(category_router)
    # app.include_router(auth)
    yield


app = FastAPI(lifespan=lifespan)
