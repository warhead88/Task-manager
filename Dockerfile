FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .

RUN apt-get update && apt-get install -y libpq-dev gcc \
    && pip install --no-cache-dir . \
    && apt-get purge -y --auto-remove gcc \
    && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["python", "-m", "src.bot"]
