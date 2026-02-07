#!/bin/bash

# Test runner script
# Usage: ./scripts/run-tests.sh [unit|integration|all]

set -e

TEST_TYPE=${1:-all}

echo "🧪 Running Tests: $TEST_TYPE"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating..."
    python3.11 -m venv venv
    source venv/bin/activate
    pip install -r backend/requirements.txt
    pip install pytest pytest-cov httpx
else
    source venv/bin/activate
fi

# Start test database
echo "📦 Starting test database..."
docker-compose -f docker-compose.test.yml up -d mysql
sleep 5

# Set test environment
export DATABASE_URL="mysql+pymysql://admin:password@localhost:3306/social_commerce_test"
export JWT_SECRET_KEY="test-secret-key-for-testing-only"
export ENVIRONMENT="test"

# Run tests
case $TEST_TYPE in
    unit)
        echo "🔬 Running unit tests..."
        pytest tests/test_*.py -v --cov=backend --cov-report=term-missing
        ;;
    integration)
        echo "🔗 Running integration tests..."
        pytest tests/integration/ -v -m integration
        ;;
    all)
        echo "🧪 Running all tests..."
        pytest tests/ -v --cov=backend --cov-report=html --cov-report=term-missing
        echo ""
        echo "📊 Coverage report generated in htmlcov/index.html"
        ;;
    *)
        echo "❌ Invalid test type. Use: unit, integration, or all"
        exit 1
        ;;
esac

# Cleanup
echo ""
echo "🧹 Cleaning up..."
docker-compose -f docker-compose.test.yml down

echo ""
echo "✅ Tests completed!"
