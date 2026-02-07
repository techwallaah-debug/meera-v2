#!/bin/bash

# Complete Deployment Script - All-in-one
# Usage: ./scripts/complete-deployment.sh [domain] [email]

set -e

DOMAIN=${1:-""}
EMAIL=${2:-""}

echo "🚀 Complete Hostinger Deployment"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Step 1: Check if project is uploaded
echo "📋 Step 1: Verifying project files..."
if [ ! -d "../../backend" ]; then
    echo "❌ Project files not found!"
    echo "   Please upload project files to /opt/social-commerce"
    exit 1
fi
echo "✅ Project files found"

# Step 2: Install prerequisites
echo ""
echo "📋 Step 2: Installing prerequisites..."
if ! command -v docker &> /dev/null; then
    echo "📦 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
fi

if ! command -v docker-compose &> /dev/null; then
    echo "📦 Installing Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi
echo "✅ Prerequisites installed"

# Step 3: Setup environment
echo ""
echo "📋 Step 3: Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Please edit .env file with your credentials"
    echo "   Run: nano .env"
    read -p "Press Enter after editing .env file..."
fi
echo "✅ Environment configured"

# Step 4: Configure domain
echo ""
if [ -z "$DOMAIN" ]; then
    read -p "Enter your domain (e.g., api.yourdomain.com): " DOMAIN
fi

if [ ! -z "$DOMAIN" ]; then
    echo "📋 Step 4: Configuring domain..."
    sed -i "s/api.yourdomain.com/${DOMAIN}/g" nginx/conf.d/api.conf
    echo "✅ Domain configured: ${DOMAIN}"
    
    # Get VPS IP
    VPS_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s icanhazip.com 2>/dev/null || echo "YOUR_VPS_IP")
    echo ""
    echo "📝 DNS Configuration Required:"
    echo "   Add A record in Hostinger:"
    echo "   Name: $(echo $DOMAIN | cut -d'.' -f1)"
    echo "   Points to: ${VPS_IP}"
    echo ""
    read -p "Press Enter after DNS is configured..."
fi

# Step 5: Setup SSL
echo ""
if [ ! -z "$DOMAIN" ] && [ ! -z "$EMAIL" ]; then
    echo "📋 Step 5: Setting up SSL certificate..."
    ./scripts/setup-ssl.sh ${DOMAIN} ${EMAIL}
    echo "✅ SSL certificate installed"
elif [ ! -z "$DOMAIN" ]; then
    read -p "Enter your email for SSL certificate: " EMAIL
    if [ ! -z "$EMAIL" ]; then
        ./scripts/setup-ssl.sh ${DOMAIN} ${EMAIL}
        echo "✅ SSL certificate installed"
    fi
fi

# Step 6: Build and start services
echo ""
echo "📋 Step 6: Building and starting services..."
docker-compose -f docker-compose.hostinger.yml build
docker-compose -f docker-compose.hostinger.yml up -d

# Wait for services
echo ""
echo "⏳ Waiting for services to start..."
sleep 30

# Step 7: Verify deployment
echo ""
echo "📋 Step 7: Verifying deployment..."
./scripts/verify-deployment.sh ${DOMAIN}

# Step 8: Test API
echo ""
echo "📋 Step 8: Testing API..."
if [ ! -z "$DOMAIN" ]; then
    ./scripts/test-api.sh ${DOMAIN}
else
    ./scripts/test-api.sh localhost
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Deployment Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
if [ ! -z "$DOMAIN" ]; then
    echo "✅ Your API is live at: https://${DOMAIN}"
else
    echo "✅ Services are running locally"
    echo "   Configure domain and SSL to access via HTTPS"
fi
echo ""
echo "📝 Useful commands:"
echo "   View logs: docker-compose -f docker-compose.hostinger.yml logs -f"
echo "   Restart: docker-compose -f docker-compose.hostinger.yml restart"
echo "   Backup: ./scripts/backup.sh"
echo "   Test API: ./scripts/test-api.sh ${DOMAIN:-localhost}"
