#!/bin/bash

# Start script for all backend services
# Usage: ./scripts/start-services.sh

echo "🚀 Starting Social Commerce Platform Services..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Run 'make setup' first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if Docker services are running
echo "📦 Checking Docker services..."
if ! docker-compose ps | grep -q "Up"; then
    echo "⚠️  Docker services not running. Starting them..."
    docker-compose up -d
    echo "⏳ Waiting for services to be ready..."
    sleep 10
fi

echo ""
echo "✅ Starting backend services..."
echo ""
echo "📝 Note: Each service will run in the foreground."
echo "   Press Ctrl+C to stop a service."
echo "   Open new terminals to run multiple services."
echo ""

# Function to start a service
start_service() {
    local service_name=$1
    local port=$2
    local path=$3
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🚀 Starting $service_name on port $port"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    cd "$path" && python main.py
}

# Menu
echo "Select service to start:"
echo "1) User Service (Port 8001)"
echo "2) Content Service (Port 8002)"
echo "3) Product Service (Port 8003)"
echo "4) All Services (requires tmux or multiple terminals)"
echo ""
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        start_service "User Service" 8001 "backend/services/user-service/src"
        ;;
    2)
        start_service "Content Service" 8002 "backend/services/content-service/src"
        ;;
    3)
        start_service "Product Service" 8003 "backend/services/product-service/src"
        ;;
    4)
        echo "To run all services, use:"
        echo "  Terminal 1: cd backend/services/user-service/src && python main.py"
        echo "  Terminal 2: cd backend/services/content-service/src && python main.py"
        echo "  Terminal 3: cd backend/services/product-service/src && python main.py"
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
