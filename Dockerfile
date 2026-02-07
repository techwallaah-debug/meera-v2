# Railway deployment - User Service
# Railway looks for Dockerfile in repo root when deploying from GitHub
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (MySQL client for pymysql)
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Use minimal requirements (file in root so build always has it)
COPY requirements-railway.txt .
RUN pip install --no-cache-dir -r requirements-railway.txt

# Copy backend (services + shared)
COPY backend/ ./backend/

# Ensure shared package is found when running from /app
ENV PYTHONPATH=/app/backend
ENV PORT=8001
EXPOSE 8001

# Run user service (Railway overrides PORT at runtime)
CMD ["python", "backend/services/user-service/src/main.py"]
