FROM python:3.12-slim

WORKDIR /app

# Copy and install shared package first
COPY shared /shared
RUN pip install -e /shared

COPY markets_collector/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY markets_collector .

CMD ["python", "src/main.py"] 