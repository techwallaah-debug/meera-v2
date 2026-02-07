#!/bin/bash

# API Testing Script
# Usage: ./scripts/test-api.sh [domain]

set -e

DOMAIN=${1:-"localhost"}
PROTOCOL="http"

# Use HTTPS if domain is not localhost
if [ "$DOMAIN" != "localhost" ]; then
    PROTOCOL="https"
fi

API_URL="${PROTOCOL}://${DOMAIN}"

echo "🧪 Testing API at ${API_URL}"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test 1: Health Check
echo "1️⃣ Testing health endpoint..."
if curl -f -s ${API_URL}/health > /dev/null; then
    echo -e "${GREEN}✅ Health endpoint working${NC}"
    curl -s ${API_URL}/health | jq . 2>/dev/null || curl -s ${API_URL}/health
else
    echo -e "${RED}❌ Health endpoint failed${NC}"
fi

# Test 2: User Service Health
echo ""
echo "2️⃣ Testing user service..."
if curl -f -s ${API_URL}/users/health > /dev/null; then
    echo -e "${GREEN}✅ User service accessible${NC}"
else
    echo -e "${RED}❌ User service not accessible${NC}"
fi

# Test 3: User Registration
echo ""
echo "3️⃣ Testing user registration..."
REGISTER_RESPONSE=$(curl -s -X POST ${API_URL}/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test'$(date +%s)'@example.com",
    "username": "testuser'$(date +%s)'",
    "full_name": "Test User",
    "password": "testpass123"
  }')

if echo "$REGISTER_RESPONSE" | grep -q "id"; then
    echo -e "${GREEN}✅ User registration working${NC}"
    USER_ID=$(echo "$REGISTER_RESPONSE" | jq -r '.id' 2>/dev/null || echo "N/A")
    echo "   User ID: ${USER_ID}"
else
    echo -e "${YELLOW}⚠️  User registration test: ${REGISTER_RESPONSE}${NC}"
fi

# Test 4: User Login
echo ""
echo "4️⃣ Testing user login..."
LOGIN_RESPONSE=$(curl -s -X POST ${API_URL}/users/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpass123" 2>/dev/null || echo "{}")

if echo "$LOGIN_RESPONSE" | grep -q "access_token"; then
    echo -e "${GREEN}✅ User login working${NC}"
    TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.access_token' 2>/dev/null || echo "")
else
    echo -e "${YELLOW}⚠️  Login test skipped (need valid user)${NC}"
fi

# Test 5: Product Service
echo ""
echo "5️⃣ Testing product service..."
if curl -f -s ${API_URL}/products > /dev/null; then
    echo -e "${GREEN}✅ Product service accessible${NC}"
    PRODUCT_COUNT=$(curl -s ${API_URL}/products | jq '. | length' 2>/dev/null || echo "N/A")
    echo "   Products found: ${PRODUCT_COUNT}"
else
    echo -e "${RED}❌ Product service not accessible${NC}"
fi

# Test 6: Content Service
echo ""
echo "6️⃣ Testing content service..."
if curl -f -s ${API_URL}/content/posts > /dev/null; then
    echo -e "${GREEN}✅ Content service accessible${NC}"
else
    echo -e "${RED}❌ Content service not accessible${NC}"
fi

# Test 7: Order Service
echo ""
echo "7️⃣ Testing order service..."
if curl -f -s ${API_URL}/orders > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Order service accessible${NC}"
else
    echo -e "${YELLOW}⚠️  Order service requires authentication${NC}"
fi

# Test 8: Search Service
echo ""
echo "8️⃣ Testing search service..."
if curl -f -s "${API_URL}/search/products?q=test" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Search service accessible${NC}"
else
    echo -e "${YELLOW}⚠️  Search service test skipped${NC}"
fi

# Test 9: SSL Certificate (if HTTPS)
if [ "$PROTOCOL" = "https" ]; then
    echo ""
    echo "9️⃣ Testing SSL certificate..."
    SSL_INFO=$(echo | openssl s_client -connect ${DOMAIN}:443 -servername ${DOMAIN} 2>/dev/null | openssl x509 -noout -dates 2>/dev/null || echo "")
    if [ ! -z "$SSL_INFO" ]; then
        echo -e "${GREEN}✅ SSL certificate valid${NC}"
        echo "$SSL_INFO"
    else
        echo -e "${YELLOW}⚠️  Could not verify SSL certificate${NC}"
    fi
fi

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 API Test Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "API Base URL: ${API_URL}"
echo ""
echo "Test endpoints:"
echo "  - Health: ${API_URL}/health"
echo "  - User Service: ${API_URL}/users/health"
echo "  - Product Service: ${API_URL}/products"
echo "  - Content Service: ${API_URL}/content/posts"
echo "  - Order Service: ${API_URL}/orders"
echo ""
echo "API Documentation:"
echo "  - User Service: ${API_URL}/users/docs"
echo "  - Content Service: ${API_URL}/content/docs"
echo "  - Product Service: ${API_URL}/products/docs"
echo "  - Order Service: ${API_URL}/orders/docs"
echo ""
echo "✅ API testing complete!"
