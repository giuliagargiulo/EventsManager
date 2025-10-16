FROM python:3.14-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
COPY ./api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /app/files && chown -R 1000:1000 /app/files
COPY . .
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
