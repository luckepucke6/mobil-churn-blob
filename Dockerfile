# Builder
FROM python:3.11-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.12.6 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-install-project --no-dev --no-editable

COPY src/ src/

RUN uv sync --locked --no-editable


# Runtime
FROM python:3.11-slim 

RUN useradd --create-home blob

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

COPY outputs/modell.joblib outputs/modell.joblib

USER blob

EXPOSE 8000

CMD ["uvicorn", "churn.api:app", "--host", "0.0.0.0", "--port", "8000"]