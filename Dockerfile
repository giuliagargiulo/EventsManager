FROM python:3.11-slim
WORKDIR /app
COPY ./api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /app/files && chown -R 1000:1000 /app/files
COPY . .
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
