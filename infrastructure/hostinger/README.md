# 🚀 Hostinger VPS Deployment Guide

Complete guide to deploy Social Commerce Platform on Hostinger VPS.

---

## 📋 Prerequisites

### Hostinger VPS Requirements:
- **VPS Plan**: At least 2GB RAM, 2 CPU cores
- **OS**: Ubuntu 20.04/22.04 or Debian 11/12
- **SSH Access**: Root or sudo access
- **Domain**: Pointed to your VPS IP (for SSL)

### Software Requirements:
- Docker 20.10+
- Docker Compose 2.0+
- 20GB+ free disk space

---

## 🚀 Quick Deployment

### Step 1: Connect to Hostinger VPS

```bash
ssh root@your-vps-ip
```

### Step 2: Clone Repository

```bash
cd /opt
git clone <your-repo-url> social-commerce
cd social-commerce
```

### Step 3: Run Deployment Script

```bash
cd infrastructure/hostinger
chmod +x scripts/*.sh
sudo ./scripts/deploy-hostinger.sh
```

The script will:
- ✅ Install Docker and Docker Compose
- ✅ Create necessary directories
- ✅ Setup environment variables
- ✅ Configure SSL (optional)
- ✅ Build and start all services

---

## 📝 Manual Deployment

### 1. Install Docker

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

### 2. Install Docker Compose

```bash
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

### 3. Setup Project

```bash
cd /opt
mkdir -p social-commerce
cd social-commerce

# Copy project files
# Upload via SFTP or git clone
```

### 4. Configure Environment

```bash
cd infrastructure/hostinger
cp .env.example .env
nano .env  # Edit with your credentials
```

**Required Variables:**
- `DB_PASSWORD` - MySQL password
- `MYSQL_ROOT_PASSWORD` - MySQL root password
- `JWT_SECRET_KEY` - Secret key for JWT tokens
- `RAZORPAY_KEY_ID` - Razorpay key
- `RAZORPAY_KEY_SECRET` - Razorpay secret

### 5. Setup SSL Certificate

```bash
# Install certbot
apt-get update
apt-get install -y certbot

# Generate certificate
./scripts/setup-ssl.sh api.yourdomain.com your@email.com

# Update nginx config with your domain
nano nginx/conf.d/api.conf
# Replace "api.yourdomain.com" with your domain
```

### 6. Start Services

```bash
# Build images
docker-compose -f docker-compose.hostinger.yml build

# Start services
docker-compose -f docker-compose.hostinger.yml up -d

# Check status
docker-compose -f docker-compose.hostinger.yml ps
```

---

## 🔧 Configuration

### Nginx Configuration

Edit `nginx/conf.d/api.conf`:
- Replace `api.yourdomain.com` with your domain
- Update SSL certificate paths if needed

### Environment Variables

Edit `.env` file with your:
- Database credentials
- API keys (Razorpay, SendGrid, Twilio)
- AWS credentials (if using S3)

### Port Configuration

Default ports:
- **80/443**: Nginx (HTTP/HTTPS)
- **3306**: MySQL (internal only)
- **6379**: Redis (internal only)

---

## 📊 Service Management

### View Logs

```bash
# All services
docker-compose -f docker-compose.hostinger.yml logs -f

# Specific service
docker-compose -f docker-compose.hostinger.yml logs -f user-service
```

### Restart Services

```bash
# Restart all
docker-compose -f docker-compose.hostinger.yml restart

# Restart specific service
docker-compose -f docker-compose.hostinger.yml restart user-service
```

### Stop Services

```bash
docker-compose -f docker-compose.hostinger.yml stop
```

### Start Services

```bash
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

Backups are stored in `/opt/social-commerce/backups/`
- Keeps last 7 backups
- Includes database, volumes, and config

### Restore Backup

```bash
./scripts/restore.sh backups/backup_20240206_120000.tar.gz
```

---

## 🔒 SSL Certificate Renewal

### Manual Renewal

```bash
certbot renew
docker-compose -f docker-compose.hostinger.yml restart nginx
```

### Auto-Renewal (Crontab)

```bash
crontab -e

# Add this line:
0 0 * * * certbot renew --quiet && cd /opt/social-commerce/infrastructure/hostinger && docker-compose -f docker-compose.hostinger.yml restart nginx
```

---

## 🏥 Health Checks

### Check Service Health

```bash
# Check all services
docker-compose -f docker-compose.hostinger.yml ps

# Test API endpoint
curl https://api.yourdomain.com/health

# Test specific service
curl https://api.yourdomain.com/users/health
```

---

## 🔍 Troubleshooting

### Services Not Starting

```bash
# Check logs
docker-compose -f docker-compose.hostinger.yml logs

# Check resource usage
docker stats

# Check disk space
df -h
```

### Database Connection Issues

```bash
# Check MySQL logs
docker-compose -f docker-compose.hostinger.yml logs mysql

# Test MySQL connection
docker exec -it mysql mysql -u admin -p
```

### Nginx Issues

```bash
# Check nginx config
docker exec nginx-proxy nginx -t

# View nginx logs
docker-compose -f docker-compose.hostinger.yml logs nginx
```

### Port Already in Use

```bash
# Check what's using port 80/443
netstat -tulpn | grep :80
netstat -tulpn | grep :443

# Stop conflicting service or change ports in docker-compose
```

---

## 📈 Performance Optimization

### Resource Limits

Edit `docker-compose.hostinger.yml` to add resource limits:

```yaml
services:
  user-service:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

### Database Optimization

```bash
# Connect to MySQL
docker exec -it mysql mysql -u root -p

# Run optimization
OPTIMIZE TABLE users, posts, products, orders;
```

### Redis Optimization

Redis is already configured with:
- Max memory: 512MB
- Eviction policy: allkeys-lru

---

## 🔐 Security Best Practices

1. **Change Default Passwords**: Update all passwords in `.env`
2. **Firewall**: Configure UFW firewall
   ```bash
   ufw allow 22/tcp
   ufw allow 80/tcp
   ufw allow 443/tcp
   ufw enable
   ```
3. **SSL**: Always use HTTPS (SSL configured)
4. **Updates**: Keep system and Docker updated
5. **Backups**: Regular automated backups

---

## 📞 Support

### Common Issues

1. **Out of Memory**: Increase VPS RAM or add swap
2. **Disk Full**: Clean old Docker images: `docker system prune -a`
3. **Slow Performance**: Check resource usage and optimize

### Getting Help

- Check logs: `docker-compose logs`
- Check service status: `docker-compose ps`
- Review configuration files

---

## ✅ Deployment Checklist

- [ ] VPS with sufficient resources (2GB+ RAM)
- [ ] Domain pointed to VPS IP
- [ ] Docker and Docker Compose installed
- [ ] Environment variables configured
- [ ] SSL certificate generated
- [ ] Services started and healthy
- [ ] Firewall configured
- [ ] Backups scheduled
- [ ] Monitoring set up

---

## 🎉 **Deployment Complete!**

Your platform is now running on Hostinger VPS!

**Access your API:**
- Production: `https://api.yourdomain.com`
- Health Check: `https://api.yourdomain.com/health`

**Next Steps:**
1. Update mobile app API URL
2. Configure domain DNS
3. Set up monitoring
4. Schedule backups

---

**🚀 Your platform is live on Hostinger!**
