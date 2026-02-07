# 🚀 Fly.io Deployment Guide

## ✅ **Deploy for FREE on Fly.io!**

Fly.io offers **3 VMs free** - perfect for your platform!

---

## 🚀 **Quick Deploy (10 Minutes)**

### Step 1: Install Fly CLI

```bash
# Mac
brew install flyctl

# Linux
curl -L https://fly.io/install.sh | sh

# Windows
# Download from https://fly.io/docs/hands-on/install-flyctl/
```

### Step 2: Sign Up

```bash
fly auth signup
# Or: fly auth login
```

### Step 3: Create App

```bash
# Navigate to project root
cd /path/to/Meera

# Launch app
fly launch

# Follow prompts:
# - App name: social-commerce-user-service
# - Region: bom (Mumbai) or closest
# - PostgreSQL: Yes (free tier)
# - Redis: Optional
```

### Step 4: Configure Environment Variables

```bash
# Set secrets
fly secrets set DATABASE_URL="postgresql://..."
fly secrets set JWT_SECRET_KEY="your-secret-key"
fly secrets set REDIS_URL="redis://..."
```

### Step 5: Deploy!

```bash
fly deploy
```

**Done! Your API is live!**

---

## 📦 **Deploy Multiple Services**

### Deploy Each Service Separately:

1. **User Service:**
   ```bash
   cd infrastructure/fly
   fly launch --name user-service
   fly deploy
   ```

2. **Content Service:**
   ```bash
   fly launch --name content-service
   fly deploy
   ```

3. **Product Service:**
   ```bash
   fly launch --name product-service
   fly deploy
   ```

4. **Order Service:**
   ```bash
   fly launch --name order-service
   fly deploy
   ```

**Each service gets its own URL!**

---

## 🗄️ **Add PostgreSQL**

```bash
# Create database
fly postgres create --name social-commerce-db

# Attach to app
fly postgres attach social-commerce-db --app user-service
```

Fly automatically sets `DATABASE_URL` environment variable!

---

## 🔧 **Custom Domain**

```bash
# Add domain
fly domains add api.yourdomain.com

# Fly auto-configures SSL!
```

---

## 📊 **Monitoring**

```bash
# View logs
fly logs

# View metrics
fly status

# SSH into VM
fly ssh console
```

---

## 💰 **Free Tier Limits**

- ✅ **3 VMs** free
- ✅ **3GB storage** free
- ✅ **160GB outbound** data transfer free
- ✅ **PostgreSQL** free (256MB)

**Perfect for MVP and testing!**

---

## 🚀 **Deploy Now!**

```bash
# 1. Install Fly CLI
brew install flyctl

# 2. Sign up
fly auth signup

# 3. Deploy
fly launch
fly deploy
```

**Done!**

---

## ✅ **Benefits:**

- ✅ **Free tier** - 3 VMs
- ✅ **Global edge** - Fast worldwide
- ✅ **PostgreSQL** - Free database
- ✅ **SSL included** - HTTPS automatically
- ✅ **Great performance** - Edge network
- ✅ **Easy scaling** - Scale up when needed

**Perfect for your platform!**
