FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PATH="/app/.venv/bin:$PATH"


WORKDIR /app


RUN pip install --no-cache-dir poetry


COPY pyproject.toml poetry.lock ./


RUN poetry install --only main --no-root --no-interaction


COPY ./src ./src


WORKDIR /app/src


EXPOSE 8000


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]