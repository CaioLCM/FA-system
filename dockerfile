FROM python:3.14

RUN ["curl", "-LsSf", "https://astral.sh/uv/install.sh", "|", "sh"]

COPY pyproject.toml .
COPY uv.lock .

RUN "uv sync"

COPY /src .

CMD ["PYTHONPATH=src", "uvicorn", "api.main:app", "--port", "8000"]