from pydantic_settings import BaseSettings, SettingsConfigDict

from typing import Annotated
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    
    openai_key: Annotated[str, Field(min_length=10)] 

    openai_model: str = "gpt-5"