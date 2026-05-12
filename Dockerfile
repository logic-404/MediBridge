FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src/ ./src/
COPY ui/ ./ui/

RUN pip install --no-cache-dir .

EXPOSE 8000

VOLUME ["/app/data", "/app/knowledge"]

ENV PYTHONUNBUFFERED=1

CMD ["medibridge"]
