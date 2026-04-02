from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

import logging

from src.database.schema import init_db

from src.api.routes.analyse import analyse
from src.api.routes.user import user
from src.api.routes.asset import asset

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
    except Exception as E:
        logger.error(f"Failed DB connection: {E}")
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health")
def get_health():
    return {"message": "on!"}

app.include_router(analyse)
app.include_router(user)
app.include_router(asset)