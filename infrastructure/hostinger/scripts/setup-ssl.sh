#!/bin/bash

# SSL Certificate Setup Script for Hostinger
# Uses Let's Encrypt Certbot

set -e

DOMAIN=${1:-"api.yourdomain.com"}
EMAIL=${2:-"admin@yourdomain.com"}

echo "🔒 Setting up SSL certificate for ${DOMAIN}"
echo ""

# Check if certbot is installed
if ! command -v certbot &> /dev/null; then
    echo "📦 Installing certbot..."
    apt-get update
    apt-get install -y certbot python3-certbot-nginx
fi

# Create SSL directory
mkdir -p nginx/ssl

# Generate certificate
echo "🔐 Generating SSL certificate..."
certbot certonly --standalone \
    --non-interactive \
    --agree-tos \
    --email ${EMAIL} \
    -d ${DOMAIN}

# Copy certificates to nginx directory
echo "📋 Copying certificates..."
cp /etc/letsencrypt/live/${DOMAIN}/fullchain.pem nginx/ssl/fullchain.pem
cp /etc/letsencrypt/live/${DOMAIN}/privkey.pem nginx/ssl/privkey.pem

# Set permissions
chmod 644 nginx/ssl/fullchain.pem
chmod 600 nginx/ssl/privkey.pem

echo ""
echo "✅ SSL certificate installed!"
echo ""
echo "📝 Certificate location:"
echo "   - Fullchain: nginx/ssl/fullchain.pem"
echo "   - Private Key: nginx/ssl/privkey.pem"
echo ""
echo "🔄 To renew certificate, run:"
echo "   certbot renew"
echo ""
echo "💡 Add to crontab for auto-renewal:"
echo "   0 0 * * * certbot renew --quiet && docker-compose restart nginx"
