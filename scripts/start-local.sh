#!/bin/bash

# Local Development Startup Script
# Usage: ./scripts/start-local.sh

set -e

echo "🏠 Starting Local Development Environment"
echo ""

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

# Start infrastructure
echo "📦 Starting infrastructure services..."
docker-compose up -d

# Wait for services
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check services
echo ""
echo "🔍 Checking services..."
docker-compose ps

# Setup Python environment
echo ""
echo "🐍 Setting up Python environment..."
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3.11 -m venv venv
fi

source venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
cd backend
pip install -q -r requirements.txt
cd ..

# Create .env if not exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created (using defaults)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Infrastructure ready!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🚀 Start services in separate terminals:"
echo ""
echo "Terminal 1 - User Service:"
echo "  cd backend/services/user-service/src && python main.py"
echo ""
echo "Terminal 2 - Content Service:"
echo "  cd backend/services/content-service/src && python main.py"
echo ""
echo "Terminal 3 - Product Service:"
echo "  cd backend/services/product-service/src && python main.py"
echo ""
echo "Terminal 4 - Order Service:"
echo "  cd backend/services/order-service/src && python main.py"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🧪 Test APIs:"
echo "  curl http://localhost:8001/health"
echo "  curl http://localhost:8002/health"
echo "  curl http://localhost:8003/health"
echo "  curl http://localhost:8004/health"
echo ""
echo "📚 API Documentation:"
echo "  http://localhost:8001/docs"
echo "  http://localhost:8002/docs"
echo "  http://localhost:8003/docs"
echo "  http://localhost:8004/docs"
echo ""
echo "🛑 Stop infrastructure:"
echo "  docker-compose down"
echo ""
