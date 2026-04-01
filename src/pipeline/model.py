from langchain_openai import ChatOpenAI
from config import Settings

settings = Settings()

model = ChatOpenAI(
    api_key=settings.openai_key,
    model=settings.openai_model,
)