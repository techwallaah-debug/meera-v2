# ⚡ Quick Start - Hostinger Deployment

## 🚀 Deploy in 5 Minutes!

### Step 1: Connect to Hostinger VPS
```bash
ssh root@your-vps-ip
```

### Step 2: Upload Project
```bash
cd /opt
# Upload project via SFTP or git clone
mkdir -p social-commerce
cd social-commerce
# Upload all project files here
```

### Step 3: Run Deployment Script
```bash
cd infrastructure/hostinger
chmod +x scripts/*.sh
sudo ./scripts/deploy-hostinger.sh
```

**The script will:**
- ✅ Install Docker & Docker Compose
- ✅ Create directories
- ✅ Setup environment
- ✅ Configure SSL
- ✅ Build and start all services

### Step 4: Configure Domain
1. Go to Hostinger hPanel
2. DNS Settings → Add A Record:
   - Name: `api`
   - Type: `A`
   - Value: Your VPS IP
   - TTL: 3600

### Step 5: Setup SSL
```bash
cd infrastructure/hostinger
./scripts/setup-ssl.sh api.yourdomain.com your@email.com
docker-compose -f docker-compose.hostinger.yml restart nginx
```

### Step 6: Test API
```bash
curl https://api.yourdomain.com/health
```

---

## ✅ Done!

**Your API is live at:** `https://api.yourdomain.com`

**View logs:**
```bash
docker-compose -f docker-compose.hostinger.yml logs -f
```

**Restart services:**
```bash
docker-compose -f docker-compose.hostinger.yml restart
```

---

**🎉 Platform is live on Hostinger!**
