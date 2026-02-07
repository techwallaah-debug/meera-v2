.PHONY: help setup start stop restart logs clean test

help:
	@echo "Available commands:"
	@echo "  make setup     - Set up the development environment"
	@echo "  make start     - Start all Docker services"
	@echo "  make stop      - Stop all Docker services"
	@echo "  make restart   - Restart all Docker services"
	@echo "  make logs      - View Docker logs"
	@echo "  make clean     - Clean up Docker volumes and containers"
	@echo "  make test      - Run tests"

setup:
	@echo "Setting up development environment..."
	python3.11 -m venv venv
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && cd backend && pip install -r requirements.txt
	@echo "Setup complete! Activate venv with: source venv/bin/activate"

start:
	@echo "Starting Docker services..."
	docker-compose up -d
	@echo "Services started! Check status with: docker-compose ps"

stop:
	@echo "Stopping Docker services..."
	docker-compose down

restart:
	@echo "Restarting Docker services..."
	docker-compose restart

logs:
	docker-compose logs -f

clean:
	@echo "Cleaning up Docker resources..."
	docker-compose down -v
	docker system prune -f

test:
	@echo "Running tests..."
	. venv/bin/activate && pytest tests/ -v

# Service-specific commands
start-user:
	cd backend/services/user-service/src && python main.py

start-content:
	cd backend/services/content-service/src && python main.py

start-product:
	cd backend/services/product-service/src && python main.py

start-all-services:
	@echo "Starting all backend services..."
	@echo "Note: Run each service in a separate terminal or use a process manager"
	@echo "User Service: make start-user"
	@echo "Content Service: make start-content"
	@echo "Product Service: make start-product"
