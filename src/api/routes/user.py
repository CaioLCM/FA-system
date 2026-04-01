from fastapi import APIRouter, HTTPException

import asyncio
from src.database.schema import create_user, get_users
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

@user.get("/")
def get_users_():
    try:
        response = get_users()
        return {"message": response}
    except Exception as E:
        logger.error(f"Erro ao buscar usuários: {E}")
        raise HTTPException(400, "Erro ao buscar usuários")
