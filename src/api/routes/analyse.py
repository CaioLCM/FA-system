from fastapi import APIRouter, Query
from src.core.asset import Asset

from src.pipeline.pipeline import pipeline 

analyse = APIRouter(prefix="/analyse", tags=["analyse"])

@analyse.post("/")
def analyse_assets(user_api: str = Query()):
    result = pipeline.invoke({"user_api": user_api})
    return {"agent_response": result["final_response"]}