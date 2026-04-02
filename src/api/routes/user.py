from fastapi import APIRouter, HTTPException

import asyncio
from src.database.schema import create_user, get_users, get_user
import secrets

import logging

logger = logging.getLogger(__name__)

user = APIRouter(prefix="/user", tags=["user"])

@user.post("/")
def create_user_(strategy: str):
    try:
        api_key = secrets.token_urlsafe(16)
        if api_key is None: raise Exception("API KEY mal gerada")
        create_user(api_key, strategy)
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

@user.get("/find")
def find_user(user_key: str):
    try:
        response = get_user(user_key)
        return {"user": response}
    except Exception as E:
        logger.error(f"Erro ao buscar usuário: {E}")
        raise HTTPException(400, "Erro ao buscar usuário")