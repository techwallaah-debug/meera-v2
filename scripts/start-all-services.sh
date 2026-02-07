#!/bin/bash

# Start all backend services script
# Usage: ./scripts/start-all-services.sh

echo "🚀 Starting All Social Commerce Platform Services..."
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
    sleep 15
fi

echo ""
echo "✅ Starting all backend services..."
echo ""
echo "📝 Note: Each service will run in a separate process."
echo "   Press Ctrl+C to stop all services."
echo ""

# Function to start a service in background
start_service_bg() {
    local service_name=$1
    local port=$2
    local path=$3
    
    echo "🚀 Starting $service_name on port $port..."
    cd "$path" && python main.py > "../../../logs/${service_name}.log" 2>&1 &
    echo "   PID: $!"
    cd - > /dev/null
}

# Create logs directory
mkdir -p logs

# Start all services
start_service_bg "User Service" 8001 "backend/services/user-service/src"
sleep 2

start_service_bg "Content Service" 8002 "backend/services/content-service/src"
sleep 2

start_service_bg "Product Service" 8003 "backend/services/product-service/src"
sleep 2

start_service_bg "Order Service" 8004 "backend/services/order-service/src"
sleep 2

start_service_bg "Search Service" 8005 "backend/services/search-service/src"
sleep 2

start_service_bg "Recommendation Service" 8006 "backend/services/recommendation-service/src"
sleep 2

start_service_bg "Analytics Service" 8007 "backend/services/analytics-service/src"
sleep 2

start_service_bg "Notification Service" 8008 "backend/services/notification-service/src"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ All services started!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Service URLs:"
echo "   User Service:        http://localhost:8001/docs"
echo "   Content Service:     http://localhost:8002/docs"
echo "   Product Service:     http://localhost:8003/docs"
echo "   Order Service:       http://localhost:8004/docs"
echo "   Search Service:      http://localhost:8005/docs"
echo "   Recommendation Svc:  http://localhost:8006/docs"
echo "   Analytics Service:   http://localhost:8007/docs"
echo "   Notification Service: http://localhost:8008/docs"
echo ""
echo "📝 Logs are in the 'logs/' directory"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
trap "echo ''; echo '🛑 Stopping all services...'; pkill -f 'python main.py'; echo '✅ All services stopped'; exit" INT

# Keep script running
wait
