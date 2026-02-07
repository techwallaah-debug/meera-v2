# ⚡ Quick Deploy - Copy & Paste Commands

## 🚀 One-Command Deployment (After Uploading Files)

```bash
cd /opt/social-commerce/infrastructure/hostinger && \
chmod +x scripts/*.sh && \
sudo ./scripts/complete-deployment.sh
```

---

## 📋 Step-by-Step Commands

### 1. Connect to VPS
```bash
ssh root@your-vps-ip
```

### 2. Upload Project (Choose one method)

**Method A: Git**
```bash
cd /opt
git clone <your-repo-url> social-commerce
cd social-commerce/infrastructure/hostinger
```

**Method B: SFTP**
- Use FileZilla/WinSCP
- Upload to `/opt/social-commerce`
- Then: `cd /opt/social-commerce/infrastructure/hostinger`

### 3. Run Complete Deployment
```bash
chmod +x scripts/*.sh
sudo ./scripts/complete-deployment.sh api.yourdomain.com your@email.com
```

**Or step by step:**

```bash
# Setup environment
cp .env.example .env
nano .env  # Edit with your credentials

# Configure domain
nano nginx/conf.d/api.conf  # Replace api.yourdomain.com

# Setup SSL
./scripts/setup-ssl.sh api.yourdomain.com your@email.com

# Deploy
docker-compose -f docker-compose.hostinger.yml up -d --build

# Verify
./scripts/verify-deployment.sh api.yourdomain.com
./scripts/test-api.sh api.yourdomain.com
```

---

## 🔍 Quick Verification

```bash
# Check services
docker-compose -f docker-compose.hostinger.yml ps

# Test API
curl https://api.yourdomain.com/health

# View logs
docker-compose -f docker-compose.hostinger.yml logs -f
```

---

## 🆘 If Something Fails

```bash
# Check logs
docker-compose -f docker-compose.hostinger.yml logs

# Restart services
docker-compose -f docker-compose.hostinger.yml restart

# Rebuild
docker-compose -f docker-compose.hostinger.yml up -d --build
```

---

**✅ That's it! Your platform is live!**
