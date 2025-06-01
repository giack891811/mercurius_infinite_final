# Dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.8.2

WORKDIR /app

# Copy project
COPY . /app

# Install deps
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["python", "-m", "core.orchestrator"]
