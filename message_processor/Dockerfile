FROM python:3.12-slim

WORKDIR /app

# Copy and install shared package first
COPY shared /shared
RUN pip install -e /shared

COPY message_processor/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY message_processor .
CMD ["python", "src/processor.py"] 