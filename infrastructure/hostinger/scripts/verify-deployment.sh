#!/bin/bash

# Verification Script - Test deployment
# Usage: ./scripts/verify-deployment.sh [domain]

set -e

DOMAIN=${1:-"api.yourdomain.com"}

echo "🔍 Verifying Deployment..."
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check Docker
echo "1️⃣ Checking Docker..."
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✅ Docker installed${NC}"
    docker --version
else
    echo -e "${RED}❌ Docker not found${NC}"
    exit 1
fi

# Check Docker Compose
echo ""
echo "2️⃣ Checking Docker Compose..."
if command -v docker-compose &> /dev/null; then
    echo -e "${GREEN}✅ Docker Compose installed${NC}"
    docker-compose --version
else
    echo -e "${RED}❌ Docker Compose not found${NC}"
    exit 1
fi

# Check running containers
echo ""
echo "3️⃣ Checking running containers..."
CONTAINERS=$(docker ps --format "{{.Names}}" | grep -E "(user-service|content-service|product-service|order-service|mysql|redis|nginx)" | wc -l)
if [ $CONTAINERS -ge 7 ]; then
    echo -e "${GREEN}✅ ${CONTAINERS} containers running${NC}"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
else
    echo -e "${YELLOW}⚠️  Only ${CONTAINERS} containers running (expected 7+)${NC}"
fi

# Check service health
echo ""
echo "4️⃣ Checking service health..."
SERVICES=("user-service:8001" "content-service:8002" "product-service:8003" "order-service:8004")
for service in "${SERVICES[@]}"; do
    IFS=':' read -r name port <<< "$service"
    if docker exec ${name} curl -f http://localhost:${port}/health &> /dev/null 2>&1; then
        echo -e "${GREEN}✅ ${name} is healthy${NC}"
    else
        echo -e "${RED}❌ ${name} health check failed${NC}"
    fi
done

# Check database
echo ""
echo "5️⃣ Checking MySQL database..."
if docker exec mysql mysql -u root -p${MYSQL_ROOT_PASSWORD} -e "SHOW DATABASES;" &> /dev/null 2>&1; then
    echo -e "${GREEN}✅ MySQL is accessible${NC}"
else
    echo -e "${YELLOW}⚠️  MySQL connection test skipped (password required)${NC}"
fi

# Check Redis
echo ""
echo "6️⃣ Checking Redis..."
if docker exec redis redis-cli ping &> /dev/null 2>&1; then
    echo -e "${GREEN}✅ Redis is accessible${NC}"
else
    echo -e "${RED}❌ Redis not responding${NC}"
fi

# Check Nginx
echo ""
echo "7️⃣ Checking Nginx..."
if docker exec nginx-proxy nginx -t &> /dev/null 2>&1; then
    echo -e "${GREEN}✅ Nginx configuration is valid${NC}"
else
    echo -e "${RED}❌ Nginx configuration has errors${NC}"
fi

# Check SSL certificate
echo ""
echo "8️⃣ Checking SSL certificate..."
if [ -f "nginx/ssl/fullchain.pem" ] && [ -f "nginx/ssl/privkey.pem" ]; then
    echo -e "${GREEN}✅ SSL certificates found${NC}"
    openssl x509 -in nginx/ssl/fullchain.pem -noout -subject -dates 2>/dev/null || echo "Certificate details unavailable"
else
    echo -e "${YELLOW}⚠️  SSL certificates not found${NC}"
fi

# Test API endpoints
echo ""
echo "9️⃣ Testing API endpoints..."
if curl -f http://localhost/health &> /dev/null 2>&1; then
    echo -e "${GREEN}✅ Local API is accessible${NC}"
else
    echo -e "${YELLOW}⚠️  Local API not accessible${NC}"
fi

# Test external domain (if provided)
if [ "$DOMAIN" != "api.yourdomain.com" ]; then
    echo ""
    echo "🔟 Testing external domain..."
    if curl -f https://${DOMAIN}/health &> /dev/null 2>&1; then
        echo -e "${GREEN}✅ External API (${DOMAIN}) is accessible${NC}"
    else
        echo -e "${YELLOW}⚠️  External API (${DOMAIN}) not accessible${NC}"
        echo "   This might be normal if DNS hasn't propagated yet"
    fi
fi

# Resource usage
echo ""
echo "📊 Resource Usage:"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

echo ""
echo "✅ Verification complete!"
echo ""
echo "📝 Summary:"
echo "   - Check logs: docker-compose -f docker-compose.hostinger.yml logs -f"
echo "   - Restart services: docker-compose -f docker-compose.hostinger.yml restart"
echo "   - View status: docker-compose -f docker-compose.hostinger.yml ps"
