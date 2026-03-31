from fastapi import FastAPI
from contextlib import asynccontextmanager

import logging

from src.database.schema import init_db

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting API")
    try:
        logger.info("Creating DB connection")
        init_db()
    except Exception as E:
        logger.error(f"Failed DB connection: {E}")
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def get_health():
    return {"message": "on!"}