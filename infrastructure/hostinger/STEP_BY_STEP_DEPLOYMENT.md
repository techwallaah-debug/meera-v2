# 📋 Step-by-Step Hostinger Deployment Guide

## Complete walkthrough for deploying to Hostinger VPS

---

## ✅ Step 1: Upload Project to Hostinger VPS

### Option A: Using Git (Recommended)

**On your local machine:**
```bash
# If you haven't initialized git yet
cd /Users/sangmeshwargurushete/Cursor/Meera
git init
git add .
git commit -m "Initial commit - Social Commerce Platform"

# Push to GitHub/GitLab
git remote add origin <your-repo-url>
git push -u origin main
```

**On Hostinger VPS:**
```bash
# Connect to VPS
ssh root@your-vps-ip

# Install Git (if not installed)
apt-get update
apt-get install -y git

# Clone repository
cd /opt
git clone <your-repo-url> social-commerce
cd social-commerce
```

### Option B: Using SFTP (FileZilla/WinSCP)

**1. Get SFTP credentials from Hostinger:**
- Host: Your VPS IP
- Port: 22
- Username: root
- Password: Your VPS password

**2. Connect using FileZilla:**
- Open FileZilla
- Enter SFTP credentials
- Navigate to `/opt` directory
- Upload entire `Meera` folder

**3. On VPS, verify upload:**
```bash
cd /opt
ls -la social-commerce
```

### Option C: Using SCP (Command Line)

**From your local machine:**
```bash
# Compress project (excluding node_modules, venv, etc.)
cd /Users/sangmeshwargurushete/Cursor
tar --exclude='node_modules' \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='.git' \
    -czf meera-project.tar.gz Meera/

# Upload to VPS
scp meera-project.tar.gz root@your-vps-ip:/opt/

# On VPS, extract
ssh root@your-vps-ip
cd /opt
tar -xzf meera-project.tar.gz
mv Meera social-commerce
cd social-commerce
```

---

## ✅ Step 2: Run Deployment Script

### Prerequisites Check

**On Hostinger VPS:**
```bash
# Make sure you're in the right directory
cd /opt/social-commerce/infrastructure/hostinger

# Check if files exist
ls -la
ls -la scripts/
```

### Run Deployment Script

```bash
# Make scripts executable
chmod +x scripts/*.sh

# Run deployment script
sudo ./scripts/deploy-hostinger.sh
```

**What the script does:**
1. ✅ Checks for Docker and Docker Compose
2. ✅ Installs if missing
3. ✅ Creates directories
4. ✅ Sets up environment file
5. ✅ Prompts for domain configuration
6. ✅ Optionally sets up SSL
7. ✅ Builds Docker images
8. ✅ Starts all services

**Expected output:**
```
🚀 Deploying Social Commerce Platform to Hostinger VPS
📋 Checking prerequisites...
✅ Prerequisites check passed
📁 Creating directories...
📋 Copying configuration files...
📝 Creating .env file...
✅ .env file created
⚠️  Please edit .env file with your actual credentials
Enter your domain name (e.g., api.yourdomain.com): 
```

### Manual Steps (if script fails)

```bash
# 1. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 2. Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# 3. Create .env file
cd /opt/social-commerce/infrastructure/hostinger
cp .env.example .env
nano .env  # Edit with your credentials

# 4. Build and start
docker-compose -f docker-compose.hostinger.yml up -d --build
```

---

## ✅ Step 3: Configure Domain DNS

### In Hostinger hPanel

**1. Login to Hostinger:**
- Go to https://hpanel.hostinger.com
- Login with your credentials

**2. Navigate to DNS Settings:**
- Click on your domain
- Go to "DNS / Name Servers"
- Click "Manage DNS Records"

**3. Add A Record:**
```
Type: A
Name: api (or your subdomain)
Points to: [Your VPS IP Address]
TTL: 3600 (or Default)
```

**4. Save Changes**

**5. Wait for DNS Propagation:**
- Usually takes 5-30 minutes
- Check propagation: https://www.whatsmydns.net

**6. Verify DNS:**
```bash
# On your local machine
nslookup api.yourdomain.com
# Should return your VPS IP
```

---

## ✅ Step 4: Setup SSL Certificate

### Option A: Using Automated Script

**On Hostinger VPS:**
```bash
cd /opt/social-commerce/infrastructure/hostinger

# Install certbot (if not installed)
apt-get update
apt-get install -y certbot

# Run SSL setup script
./scripts/setup-ssl.sh api.yourdomain.com your@email.com
```

**The script will:**
- ✅ Generate Let's Encrypt certificate
- ✅ Copy certificates to nginx directory
- ✅ Set proper permissions

### Option B: Manual SSL Setup

```bash
# 1. Stop nginx temporarily (if running)
docker-compose -f docker-compose.hostinger.yml stop nginx

# 2. Generate certificate
certbot certonly --standalone \
    --non-interactive \
    --agree-tos \
    --email your@email.com \
    -d api.yourdomain.com

# 3. Copy certificates
mkdir -p nginx/ssl
cp /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem nginx/ssl/fullchain.pem
cp /etc/letsencrypt/live/api.yourdomain.com/privkey.pem nginx/ssl/privkey.pem

# 4. Set permissions
chmod 644 nginx/ssl/fullchain.pem
chmod 600 nginx/ssl/privkey.pem

# 5. Update nginx config with your domain
nano nginx/conf.d/api.conf
# Replace "api.yourdomain.com" with your actual domain

# 6. Start nginx
docker-compose -f docker-compose.hostinger.yml start nginx
```

### Setup Auto-Renewal

```bash
# Add to crontab
crontab -e

# Add this line (runs daily at midnight)
0 0 * * * certbot renew --quiet && cd /opt/social-commerce/infrastructure/hostinger && docker-compose -f docker-compose.hostinger.yml restart nginx
```

---

## ✅ Step 5: Test Your API

### Test Health Endpoints

```bash
# Test main health endpoint
curl https://api.yourdomain.com/health

# Test user service
curl https://api.yourdomain.com/users/health

# Test product service
curl https://api.yourdomain.com/products

# Test with authentication
curl -X POST https://api.yourdomain.com/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "full_name": "Test User",
    "password": "testpass123"
  }'
```

### Test from Browser

**Open in browser:**
- Health: `https://api.yourdomain.com/health`
- API Docs: `https://api.yourdomain.com/users/docs`

### Test from Mobile App

**Update API URL in mobile app:**
```typescript
// frontend/mobile/src/services/api.ts
const API_BASE_URL = 'https://api.yourdomain.com';
```

---

## 🔍 Troubleshooting

### Services Not Starting

```bash
# Check logs
docker-compose -f docker-compose.hostinger.yml logs

# Check specific service
docker-compose -f docker-compose.hostinger.yml logs user-service

# Check if ports are available
netstat -tulpn | grep :80
netstat -tulpn | grep :443
```

### Database Connection Issues

```bash
# Check MySQL logs
docker-compose -f docker-compose.hostinger.yml logs mysql

# Test MySQL connection
docker exec -it mysql mysql -u admin -p
# Enter password from .env file
```

### SSL Certificate Issues

```bash
# Check certificate
certbot certificates

# Renew certificate manually
certbot renew

# Check nginx config
docker exec nginx-proxy nginx -t
```

### Domain Not Resolving

```bash
# Check DNS
nslookup api.yourdomain.com

# Check if domain points to correct IP
dig api.yourdomain.com +short
# Should return your VPS IP
```

---

## ✅ Verification Checklist

- [ ] Project files uploaded to `/opt/social-commerce`
- [ ] Docker and Docker Compose installed
- [ ] `.env` file configured with credentials
- [ ] All services started successfully
- [ ] Domain DNS configured (A record)
- [ ] SSL certificate generated
- [ ] Nginx running and accessible
- [ ] Health endpoints responding
- [ ] API endpoints working
- [ ] Mobile app can connect

---

## 🎉 **Deployment Complete!**

**Your API is now live at:**
- `https://api.yourdomain.com`

**Test it:**
```bash
curl https://api.yourdomain.com/health
```

**View logs:**
```bash
docker-compose -f docker-compose.hostinger.yml logs -f
```

---

**🚀 Your platform is live on Hostinger!**
