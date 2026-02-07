#!/bin/bash

# DNS Setup Guide Script
# This script provides instructions for DNS configuration

echo "🌐 DNS Configuration Guide for Hostinger"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Get VPS IP
VPS_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s icanhazip.com 2>/dev/null || echo "YOUR_VPS_IP")

echo "📋 Your VPS IP Address: ${VPS_IP}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 Steps to Configure DNS in Hostinger:"
echo ""
echo "1️⃣  Login to Hostinger hPanel:"
echo "   → https://hpanel.hostinger.com"
echo ""
echo "2️⃣  Navigate to DNS Settings:"
echo "   → Click on your domain"
echo "   → Go to 'DNS / Name Servers'"
echo "   → Click 'Manage DNS Records'"
echo ""
echo "3️⃣  Add A Record:"
echo "   ┌─────────────────────────────────────────────┐"
echo "   │ Type:        A                             │"
echo "   │ Name:        api (or your subdomain)       │"
echo "   │ Points to:   ${VPS_IP}"
echo "   │ TTL:         3600 (or Default)            │"
echo "   └─────────────────────────────────────────────┘"
echo ""
echo "4️⃣  Click 'Add Record' or 'Save'"
echo ""
echo "5️⃣  Wait for DNS Propagation (5-30 minutes)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🔍 Verify DNS Configuration:"
echo ""
echo "   # Check DNS propagation"
echo "   nslookup api.yourdomain.com"
echo ""
echo "   # Or use online tool"
echo "   https://www.whatsmydns.net"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📝 Example DNS Records:"
echo ""
echo "   For API subdomain:"
echo "   api.yourdomain.com → ${VPS_IP}"
echo ""
echo "   For main domain (optional):"
echo "   yourdomain.com → ${VPS_IP}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Enter your domain name (e.g., yourdomain.com): " DOMAIN
read -p "Enter your subdomain (e.g., api): " SUBDOMAIN

if [ ! -z "$DOMAIN" ] && [ ! -z "$SUBDOMAIN" ]; then
    FULL_DOMAIN="${SUBDOMAIN}.${DOMAIN}"
    echo ""
    echo "✅ Your API will be accessible at:"
    echo "   https://${FULL_DOMAIN}"
    echo ""
    echo "📝 DNS Record to add:"
    echo "   Type: A"
    echo "   Name: ${SUBDOMAIN}"
    echo "   Points to: ${VPS_IP}"
    echo "   TTL: 3600"
    echo ""
    
    # Update nginx config
    if [ -f "nginx/conf.d/api.conf" ]; then
        echo "🔄 Updating nginx configuration..."
        sed -i "s/api.yourdomain.com/${FULL_DOMAIN}/g" nginx/conf.d/api.conf
        echo "✅ Nginx config updated with ${FULL_DOMAIN}"
    fi
fi

echo ""
echo "✅ DNS setup guide complete!"
echo ""
echo "💡 After DNS propagates, run:"
echo "   ./scripts/setup-ssl.sh ${FULL_DOMAIN} your@email.com"
