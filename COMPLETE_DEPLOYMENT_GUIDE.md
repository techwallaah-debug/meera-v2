# 🚀 Complete Deployment Guide - Hostinger VPS

## ✅ **ALL DEPLOYMENT STEPS READY!**

---

## 📋 Overview

This guide covers all 5 steps:
1. ✅ Upload project to Hostinger VPS
2. ✅ Run deployment script
3. ✅ Configure domain DNS
4. ✅ Setup SSL certificate
5. ✅ Test API

---

## 🚀 Step 1: Upload Project to Hostinger VPS

### Method 1: Using Git (Recommended)

**On your local machine (if not already done):**
```bash
cd /Users/sangmeshwargurushete/Cursor/Meera
git init
git add .
git commit -m "Social Commerce Platform - Ready for deployment"

# Push to GitHub/GitLab/Bitbucket
git remote add origin <your-repo-url>
git push -u origin main
```

**On Hostinger VPS:**
```bash
# Connect via SSH
ssh root@your-vps-ip

# Install Git (if needed)
apt-get update && apt-get install -y git

# Clone repository
cd /opt
git clone <your-repo-url> social-commerce
cd social-commerce/infrastructure/hostinger
```

### Method 2: Using SFTP (FileZilla)

**1. Get SFTP Details from Hostinger:**
- Host: Your VPS IP address
- Port: 22
- Username: root
- Password: Your VPS root password

**2. Connect with FileZilla:**
- Open FileZilla
- File → Site Manager → New Site
- Enter SFTP details
- Connect

**3. Upload Files:**
- Navigate to `/opt` on server
- Upload entire `Meera` folder
- Rename to `social-commerce` if needed

**4. Verify Upload:**
```bash
ssh root@your-vps-ip
cd /opt/social-commerce
ls -la
# Should see: backend, frontend, infrastructure, etc.
```

### Method 3: Using SCP (Command Line)

**From your local machine:**
```bash
# Create archive (excluding unnecessary files)
cd /Users/sangmeshwargurushete/Cursor
tar --exclude='node_modules' \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='.git' \
    --exclude='*.pyc' \
    -czf meera-deploy.tar.gz Meera/

# Upload to VPS
scp meera-deploy.tar.gz root@your-vps-ip:/opt/

# Extract on VPS
ssh root@your-vps-ip
cd /opt
tar -xzf meera-deploy.tar.gz
mv Meera social-commerce
cd social-commerce/infrastructure/hostinger
```

---

## 🔧 Step 2: Run Deployment Script

### Quick Deploy (All-in-One)

```bash
cd /opt/social-commerce/infrastructure/hostinger
chmod +x scripts/*.sh
sudo ./scripts/complete-deployment.sh api.yourdomain.com your@email.com
```

### Manual Deploy (Step-by-Step)

```bash
# 1. Make scripts executable
chmod +x scripts/*.sh

# 2. Run main deployment script
sudo ./scripts/deploy-hostinger.sh

# Follow prompts:
# - Enter domain name when asked
# - Choose to setup SSL (y/n)
# - Enter email for SSL certificate
```

**What happens:**
- ✅ Installs Docker & Docker Compose
- ✅ Creates directories
- ✅ Sets up `.env` file
- ✅ Configures domain in nginx
- ✅ Sets up SSL (if chosen)
- ✅ Builds Docker images
- ✅ Starts all services

### If Script Fails

**Manual installation:**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Setup environment
cp .env.example .env
nano .env  # Edit with your credentials

# Build and start
docker-compose -f docker-compose.hostinger.yml up -d --build
```

---

## 🌐 Step 3: Configure Domain DNS

### In Hostinger hPanel

**1. Login:**
- Go to https://hpanel.hostinger.com
- Login with your Hostinger account

**2. Navigate to DNS:**
- Click on your domain name
- Go to "DNS / Name Servers" section
- Click "Manage DNS Records" or "DNS Zone Editor"

**3. Add A Record:**
```
┌─────────────────────────────────────────┐
│ Type:        A                           │
│ Name:        api (or your subdomain)     │
│ Points to:   [Your VPS IP Address]      │
│ TTL:         3600 (or Default)          │
└─────────────────────────────────────────┘
```

**4. Save the record**

**5. Get your VPS IP:**
```bash
# On VPS, run:
curl ifconfig.me
# Or check Hostinger VPS panel
```

**6. Wait for DNS Propagation:**
- Usually 5-30 minutes
- Check: https://www.whatsmydns.net

**7. Verify DNS:**
```bash
# On your local machine
nslookup api.yourdomain.com
# Should return your VPS IP

# Or use dig
dig api.yourdomain.com +short
```

**Helper Script:**
```bash
cd /opt/social-commerce/infrastructure/hostinger
./scripts/setup-dns-guide.sh
```

---

## 🔒 Step 4: Setup SSL Certificate

### Automated Setup

```bash
cd /opt/social-commerce/infrastructure/hostinger

# Run SSL setup script
./scripts/setup-ssl.sh api.yourdomain.com your@email.com

# Restart nginx
docker-compose -f docker-compose.hostinger.yml restart nginx
```

### Manual Setup

```bash
# 1. Install certbot
apt-get update
apt-get install -y certbot

# 2. Stop nginx temporarily
docker-compose -f docker-compose.hostinger.yml stop nginx

# 3. Generate certificate
certbot certonly --standalone \
    --non-interactive \
    --agree-tos \
    --email your@email.com \
    -d api.yourdomain.com

# 4. Copy certificates
mkdir -p nginx/ssl
cp /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem nginx/ssl/
cp /etc/letsencrypt/live/api.yourdomain.com/privkey.pem nginx/ssl/

# 5. Set permissions
chmod 644 nginx/ssl/fullchain.pem
chmod 600 nginx/ssl/privkey.pem

# 6. Update nginx config (if not done)
nano nginx/conf.d/api.conf
# Replace "api.yourdomain.com" with your domain

# 7. Start nginx
docker-compose -f docker-compose.hostinger.yml start nginx
```

### Auto-Renewal Setup

```bash
# Edit crontab
crontab -e

# Add this line (runs daily at midnight)
0 0 * * * certbot renew --quiet && cd /opt/social-commerce/infrastructure/hostinger && docker-compose -f docker-compose.hostinger.yml restart nginx
```

---

## 🧪 Step 5: Test Your API

### Quick Test Script

```bash
cd /opt/social-commerce/infrastructure/hostinger
./scripts/test-api.sh api.yourdomain.com
```

### Manual Testing

**1. Health Check:**
```bash
curl https://api.yourdomain.com/health
```

**2. User Service:**
```bash
curl https://api.yourdomain.com/users/health
```

**3. Register User:**
```bash
curl -X POST https://api.yourdomain.com/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "full_name": "Test User",
    "password": "testpass123"
  }'
```

**4. Login:**
```bash
curl -X POST https://api.yourdomain.com/users/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpass123"
```

**5. Get Products:**
```bash
curl https://api.yourdomain.com/products
```

**6. API Documentation:**
Open in browser:
- `https://api.yourdomain.com/users/docs`
- `https://api.yourdomain.com/products/docs`
- `https://api.yourdomain.com/orders/docs`

### Verification Script

```bash
./scripts/verify-deployment.sh api.yourdomain.com
```

---

## ✅ Complete Verification

### Check All Services

```bash
# View running containers
docker-compose -f docker-compose.hostinger.yml ps

# Should see:
# - user-service (running)
# - content-service (running)
# - product-service (running)
# - order-service (running)
# - mysql (running)
# - redis (running)
# - nginx-proxy (running)
```

### Check Logs

```bash
# All services
docker-compose -f docker-compose.hostinger.yml logs -f

# Specific service
docker-compose -f docker-compose.hostinger.yml logs -f user-service
```

### Check Resource Usage

```bash
docker stats --no-stream
```

---

## 🎉 **Deployment Complete!**

**Your API is now live at:**
- `https://api.yourdomain.com`

**Test it:**
```bash
curl https://api.yourdomain.com/health
```

**Access API Docs:**
- `https://api.yourdomain.com/users/docs`

---

## 📝 Quick Reference

### Useful Commands

```bash
# View status
docker-compose -f docker-compose.hostinger.yml ps

# View logs
docker-compose -f docker-compose.hostinger.yml logs -f

# Restart services
docker-compose -f docker-compose.hostinger.yml restart

# Stop services
docker-compose -f docker-compose.hostinger.yml stop

# Start services
docker-compose -f docker-compose.hostinger.yml start

# Backup
./scripts/backup.sh

# Test API
./scripts/test-api.sh api.yourdomain.com

# Verify deployment
./scripts/verify-deployment.sh api.yourdomain.com
```

---

## 🆘 Troubleshooting

### Services Not Starting
```bash
# Check logs
docker-compose -f docker-compose.hostinger.yml logs

# Check disk space
df -h

# Check memory
free -h
```

### SSL Issues
```bash
# Check certificate
certbot certificates

# Renew manually
certbot renew
```

### DNS Not Working
```bash
# Check DNS
nslookup api.yourdomain.com

# Verify IP matches
curl ifconfig.me
```

---

**🚀 Your platform is live on Hostinger!**

**Need help?** Check the detailed guides in `infrastructure/hostinger/README.md`
