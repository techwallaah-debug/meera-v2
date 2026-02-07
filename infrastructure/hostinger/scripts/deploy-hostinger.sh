#!/bin/bash

# Hostinger VPS Deployment Script
# Usage: ./scripts/deploy-hostinger.sh

set -e

echo "🚀 Deploying Social Commerce Platform to Hostinger VPS"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}❌ Please run as root or with sudo${NC}"
    exit 1
fi

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker not found. Installing Docker...${NC}"
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}⚠️  Docker Compose not found. Installing...${NC}"
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"

# Create directories
echo ""
echo "📁 Creating directories..."
mkdir -p /opt/social-commerce/{nginx/ssl,nginx/logs,nginx/conf.d,mysql/data,redis/data,elasticsearch/data}
cd /opt/social-commerce

# Copy configuration files
echo "📋 Copying configuration files..."
# Assuming script is run from project root
cp -r infrastructure/hostinger/* .

# Create .env file if not exists
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file..."
    cat > .env << EOF
# Database
DB_NAME=social_commerce
DB_USER=admin
DB_PASSWORD=$(openssl rand -base64 32)
MYSQL_ROOT_PASSWORD=$(openssl rand -base64 32)

# JWT
JWT_SECRET_KEY=$(openssl rand -base64 64)

# AWS (Optional - for S3)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
S3_BUCKET_NAME=social-commerce-media

# Payment Gateway
RAZORPAY_KEY_ID=your-razorpay-key
RAZORPAY_KEY_SECRET=your-razorpay-secret

# Email/SMS
SENDGRID_API_KEY=your-sendgrid-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token

# Environment
ENVIRONMENT=production
DEBUG=False
EOF
    echo -e "${GREEN}✅ .env file created${NC}"
    echo -e "${YELLOW}⚠️  Please edit .env file with your actual credentials${NC}"
fi

# Update domain in nginx config
read -p "Enter your domain name (e.g., api.yourdomain.com): " DOMAIN
if [ ! -z "$DOMAIN" ]; then
    sed -i "s/api.yourdomain.com/${DOMAIN}/g" nginx/conf.d/api.conf
    echo -e "${GREEN}✅ Domain updated in nginx config${NC}"
fi

# Setup SSL
read -p "Do you want to setup SSL certificate? (y/n): " SETUP_SSL
if [ "$SETUP_SSL" = "y" ]; then
    read -p "Enter your email for SSL certificate: " EMAIL
    ./scripts/setup-ssl.sh ${DOMAIN} ${EMAIL}
fi

# Build and start services
echo ""
echo "🔨 Building Docker images..."
docker-compose -f docker-compose.hostinger.yml build

echo ""
echo "🚀 Starting services..."
docker-compose -f docker-compose.hostinger.yml up -d

# Wait for services to be ready
echo ""
echo "⏳ Waiting for services to start..."
sleep 30

# Check service health
echo ""
echo "🏥 Checking service health..."
SERVICES=("user-service:8001" "content-service:8002" "product-service:8003" "order-service:8004")
for service in "${SERVICES[@]}"; do
    IFS=':' read -r name port <<< "$service"
    if docker exec ${name} curl -f http://localhost:${port}/health &> /dev/null; then
        echo -e "${GREEN}✅ ${name} is healthy${NC}"
    else
        echo -e "${YELLOW}⚠️  ${name} health check failed${NC}"
    fi
done

# Show status
echo ""
echo "📊 Service Status:"
docker-compose -f docker-compose.hostinger.yml ps

echo ""
echo -e "${GREEN}🎉 Deployment complete!${NC}"
echo ""
echo "📝 Next steps:"
echo "1. Update DNS A record to point to this server's IP"
echo "2. Access API at: https://${DOMAIN}"
echo "3. View logs: docker-compose -f docker-compose.hostinger.yml logs -f"
echo "4. Stop services: docker-compose -f docker-compose.hostinger.yml down"
echo "5. Restart services: docker-compose -f docker-compose.hostinger.yml restart"
