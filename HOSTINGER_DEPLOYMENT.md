# 🚀 Hostinger VPS Deployment - Complete Guide

## ✅ **HOSTINGER DEPLOYMENT READY!**

---

## 📋 What's Included

### ✅ Complete Hostinger Configuration
- ✅ Docker Compose setup
- ✅ Nginx reverse proxy
- ✅ SSL certificate setup (Let's Encrypt)
- ✅ Automated deployment script
- ✅ Backup and restore scripts
- ✅ Health checks
- ✅ Service management

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Connect to Hostinger VPS

```bash
ssh root@your-vps-ip
# Or use Hostinger's web terminal
```

### Step 2: Upload Project Files

**Option A: Using Git**
```bash
cd /opt
git clone <your-repo-url> social-commerce
cd social-commerce
```

**Option B: Using SFTP**
- Use FileZilla or WinSCP
- Upload entire project to `/opt/social-commerce`

### Step 3: Run Deployment

```bash
cd infrastructure/hostinger
chmod +x scripts/*.sh
sudo ./scripts/deploy-hostinger.sh
```

**That's it!** The script handles everything.

---

## 📝 Detailed Steps

### 1. Prerequisites Check

**VPS Requirements:**
- ✅ Ubuntu 20.04/22.04 or Debian 11/12
- ✅ 2GB+ RAM (4GB recommended)
- ✅ 2+ CPU cores
- ✅ 20GB+ disk space
- ✅ Root or sudo access

### 2. Install Docker (if not installed)

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

### 3. Install Docker Compose

```bash
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

### 4. Setup Project

```bash
cd /opt
mkdir -p social-commerce
cd social-commerce

# Upload your project files here
# Or clone from git
```

### 5. Configure Environment

```bash
cd infrastructure/hostinger
cp .env.example .env
nano .env  # Edit with your credentials
```

**Important Variables:**
```env
DB_PASSWORD=your_strong_password_here
MYSQL_ROOT_PASSWORD=your_root_password_here
JWT_SECRET_KEY=your_very_long_secret_key_here
RAZORPAY_KEY_ID=your_razorpay_key
RAZORPAY_KEY_SECRET=your_razorpay_secret
```

### 6. Setup Domain & SSL

**Update Nginx Config:**
```bash
nano nginx/conf.d/api.conf
# Replace "api.yourdomain.com" with your actual domain
```

**Generate SSL Certificate:**
```bash
./scripts/setup-ssl.sh api.yourdomain.com your@email.com
```

### 7. Deploy

```bash
# Build and start all services
docker-compose -f docker-compose.hostinger.yml up -d --build

# Check status
docker-compose -f docker-compose.hostinger.yml ps
```

---

## 🔧 Service Management

### View Logs
```bash
# All services
docker-compose -f docker-compose.hostinger.yml logs -f

# Specific service
docker-compose -f docker-compose.hostinger.yml logs -f user-service
```

### Restart Services
```bash
# All services
docker-compose -f docker-compose.hostinger.yml restart

# Specific service
docker-compose -f docker-compose.hostinger.yml restart user-service
```

### Stop/Start Services
```bash
# Stop
docker-compose -f docker-compose.hostinger.yml stop

# Start
docker-compose -f docker-compose.hostinger.yml start
```

### Update Services
```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose -f docker-compose.hostinger.yml up -d --build
```

---

## 💾 Backup & Restore

### Create Backup
```bash
./scripts/backup.sh
```

**Backup includes:**
- MySQL database dump
- Docker volumes (MySQL, Redis data)
- Configuration files
- Stored in `/opt/social-commerce/backups/`
- Keeps last 7 backups automatically

### Restore Backup
```bash
./scripts/restore.sh backups/backup_20240206_120000.tar.gz
```

### Schedule Automatic Backups

Add to crontab:
```bash
crontab -e

# Daily backup at 2 AM
0 2 * * * cd /opt/social-commerce/infrastructure/hostinger && ./scripts/backup.sh
```

---

## 🔒 SSL Certificate Management

### Renew Certificate
```bash
certbot renew
docker-compose -f docker-compose.hostinger.yml restart nginx
```

### Auto-Renewal Setup
```bash
crontab -e

# Add this line (runs daily at midnight)
0 0 * * * certbot renew --quiet && cd /opt/social-commerce/infrastructure/hostinger && docker-compose -f docker-compose.hostinger.yml restart nginx
```

---

## 🏥 Health Checks

### Check All Services
```bash
docker-compose -f docker-compose.hostinger.yml ps
```

### Test API Endpoints
```bash
# Health check
curl https://api.yourdomain.com/health

# User service
curl https://api.yourdomain.com/users/health

# Product service
curl https://api.yourdomain.com/products
```

---

## 🔍 Troubleshooting

### Services Not Starting

```bash
# Check logs
docker-compose -f docker-compose.hostinger.yml logs

# Check specific service
docker-compose -f docker-compose.hostinger.yml logs user-service

# Check resource usage
docker stats
```

### Database Issues

```bash
# Check MySQL logs
docker-compose -f docker-compose.hostinger.yml logs mysql

# Connect to MySQL
docker exec -it mysql mysql -u admin -p

# Check database
SHOW DATABASES;
USE social_commerce;
SHOW TABLES;
```

### Nginx Issues

```bash
# Test nginx config
docker exec nginx-proxy nginx -t

# View nginx logs
docker-compose -f docker-compose.hostinger.yml logs nginx

# Reload nginx
docker exec nginx-proxy nginx -s reload
```

### Port Conflicts

```bash
# Check what's using ports
netstat -tulpn | grep :80
netstat -tulpn | grep :443

# If Hostinger's default web server is running, stop it
systemctl stop apache2  # or nginx
systemctl disable apache2
```

### Out of Memory

```bash
# Check memory usage
free -h
docker stats

# Add swap space (if needed)
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

### Disk Space Issues

```bash
# Check disk usage
df -h

# Clean Docker
docker system prune -a

# Remove old backups
cd backups && ls -t | tail -n +8 | xargs rm -f
```

---

## 🔐 Security Setup

### 1. Configure Firewall (UFW)

```bash
# Install UFW
apt-get install ufw

# Allow SSH, HTTP, HTTPS
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp

# Enable firewall
ufw enable

# Check status
ufw status
```

### 2. Change Default Passwords

Update all passwords in `.env` file:
- Database passwords
- JWT secret key
- API keys

### 3. Secure SSH

```bash
# Disable root login (optional)
nano /etc/ssh/sshd_config
# Set: PermitRootLogin no

# Use SSH keys instead of passwords
# Restart SSH
systemctl restart sshd
```

### 4. Regular Updates

```bash
# Update system
apt-get update && apt-get upgrade -y

# Update Docker images
docker-compose -f docker-compose.hostinger.yml pull
docker-compose -f docker-compose.hostinger.yml up -d
```

---

## 📊 Monitoring

### Resource Usage

```bash
# CPU and Memory
htop  # or top

# Docker stats
docker stats

# Disk usage
df -h
du -sh /opt/social-commerce/*
```

### Service Health

```bash
# Check all services
docker-compose -f docker-compose.hostinger.yml ps

# Check specific service health
docker exec user-service curl http://localhost:8001/health
```

---

## 🎯 Performance Optimization

### 1. Database Optimization

```bash
# Connect to MySQL
docker exec -it mysql mysql -u root -p

# Optimize tables
OPTIMIZE TABLE users, posts, products, orders, carts;
ANALYZE TABLE users, posts, products, orders, carts;
```

### 2. Redis Optimization

Already configured with:
- Max memory: 512MB
- Eviction policy: allkeys-lru
- Persistence: AOF enabled

### 3. Nginx Optimization

Already configured with:
- Gzip compression
- Keep-alive connections
- Rate limiting
- Caching headers

### 4. Resource Limits

Edit `docker-compose.hostinger.yml` to add limits:

```yaml
services:
  user-service:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

---

## 📞 Hostinger-Specific Notes

### Hostinger VPS Features:
- ✅ Full root access
- ✅ Docker support
- ✅ Custom domain support
- ✅ SSL certificate support
- ✅ Backup options

### Hostinger Control Panel:
- Use Hostinger's hPanel for:
  - DNS management
  - Domain configuration
  - Basic server management

### DNS Configuration:
1. Go to Hostinger hPanel
2. Navigate to DNS settings
3. Add A record:
   - Name: `api` (or subdomain)
   - Type: `A`
   - Value: Your VPS IP address
   - TTL: 3600

---

## ✅ Deployment Checklist

- [ ] VPS purchased from Hostinger
- [ ] SSH access configured
- [ ] Domain pointed to VPS IP
- [ ] Docker installed
- [ ] Project files uploaded
- [ ] Environment variables configured
- [ ] SSL certificate generated
- [ ] Services started successfully
- [ ] Health checks passing
- [ ] Firewall configured
- [ ] Backups scheduled
- [ ] Monitoring set up

---

## 🎉 **Deployment Complete!**

**Your API is now live at:**
- `https://api.yourdomain.com`

**Test it:**
```bash
curl https://api.yourdomain.com/health
curl https://api.yourdomain.com/users/health
```

**Next Steps:**
1. Update mobile app API URL to your domain
2. Test all endpoints
3. Set up monitoring
4. Schedule backups
5. Configure alerts

---

## 📚 Additional Resources

- `infrastructure/hostinger/README.md` - Detailed guide
- `infrastructure/hostinger/scripts/` - Deployment scripts
- `infrastructure/hostinger/nginx/` - Nginx configurations

---

**🚀 Your platform is now running on Hostinger VPS!**

**Need help?** Check the troubleshooting section or review logs.
