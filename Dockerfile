FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY pyproject.toml .
COPY phoenix_core ./phoenix_core

RUN python -c "import phoenix_core; print('PHOENIX import: OK')"

EXPOSE 8000

CMD ["uvicorn", "phoenix_core.http_api:app", "--host", "0.0.0.0", "--port", "8000"]
