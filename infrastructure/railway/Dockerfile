# Railway Deployment Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY .env.example .env

# Expose port (Railway will set PORT env var)
EXPOSE 8001

# Start service (Railway will override with startCommand)
CMD ["python", "backend/services/user-service/src/main.py"]
