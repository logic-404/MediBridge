FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV MEDIBRIDGE_ROOT=/app

COPY pyproject.toml README.md ./
COPY src/ ./src/
COPY ui/ ./ui/
COPY data/ ./data/

RUN pip install --no-cache-dir .

EXPOSE 8000

COPY docker-entrypoint.sh ./
RUN chmod +x docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["medibridge"]
