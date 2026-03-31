FROM python:3.13

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync

COPY . .

ENV PYTHONPATH=src

CMD ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]