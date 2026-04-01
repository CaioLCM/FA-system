from fastapi import APIRouter
from src.core.asset import Asset

from src.pipeline.pipeline import pipeline 

analyse = APIRouter(prefix="/analyse", tags=["analyse"])

@analyse.post("/")
def analyse_assets(assets: list[Asset]):
    result = pipeline.invoke({"assets": assets})
    return {"agent_response": result["final_response"]}