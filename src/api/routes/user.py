from fastapi import APIRouter, HTTPException

import asyncio
from src.database.schema import create_user
import secrets

import logging

logger = logging.getLogger(__name__)

user = APIRouter(prefix="/user", tags=["user"])

@user.post("/")
def create_user_():
    try:
        api_key = secrets.token_urlsafe(16)
        if api_key is None: raise Exception("API KEY mal gerada")
        create_user(api_key)
        return {"message": f"API KEY para o seu usuário (guarde com carinho): {api_key}"}
    except Exception as E:
        raise HTTPException(400, "Erro ao criar usuário")