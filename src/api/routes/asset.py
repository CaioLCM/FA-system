from fastapi import APIRouter, HTTPException, Query

from src.core.asset import Asset
from src.database.schema import create_asset, get_assets

import logging

logger = logging.getLogger(__name__)

asset = APIRouter(prefix="/asset", tags=["asset"])

@asset.post("/")
def create_asset_(user_api: str = Query(...), body: Asset = ...):
    try:
        create_asset(user_api, body)
        return {"message": f"Asset '{body.name}' criado com sucesso"}
    except ValueError as e:
        raise HTTPException(401, "user_api inválida")
    except Exception as e:
        logger.error(f"Erro ao criar asset: {e}")
        raise HTTPException(400, "Erro ao criar asset")

@asset.get("/")
def get_assets_(user_api: str = Query(...)):
    try:
        response = get_assets(user_api)
        return {"message": response}
    except Exception as e:
        logger.error(f"Erro ao buscar assets: {e}")
        raise HTTPException(400, "Erro ao buscar assets")
