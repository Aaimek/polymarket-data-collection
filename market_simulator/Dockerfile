FROM python:3.12-slim

WORKDIR /app

# Copy and install shared package first
COPY shared /shared
RUN pip install -e /shared


COPY market_simulator/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY market_simulator .

CMD ["python", "src/main.py"] 