# 🎨 Render.com Deployment Guide

## ✅ **Deploy for FREE on Render!**

Render offers **free tier** - perfect for your platform!

---

## 🚀 **Quick Deploy (15 Minutes)**

### Step 1: Sign Up

1. Go to https://render.com
2. Sign up with GitHub (free)
3. Verify email

### Step 2: Create Database

1. Click **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name:** social-commerce-db
   - **Database:** social_commerce
   - **User:** admin
   - **Plan:** Free
3. Click **"Create Database"**
4. Copy **Internal Database URL** (for services)
5. Copy **External Database URL** (for local access)

### Step 3: Deploy User Service

1. Click **"New +"** → **"Web Service"**
2. Connect GitHub repository
3. Configure:
   - **Name:** user-service
   - **Environment:** Python 3
   - **Region:** Singapore (or closest)
   - **Branch:** main
   - **Root Directory:** (leave empty)
   - **Build Command:** `cd backend && pip install -r requirements.txt`
   - **Start Command:** `cd backend/services/user-service/src && python main.py`
4. Click **"Advanced"** → **"Add Environment Variable"**:
   ```
   DATABASE_URL=<paste Internal Database URL>
   JWT_SECRET_KEY=your-super-secret-key
   PORT=8001
   ```
5. Click **"Create Web Service"**

### Step 4: Deploy Other Services

Repeat Step 3 for:
- **Content Service** (port 8002)
- **Product Service** (port 8003)
- **Order Service** (port 8004)

**Each service gets its own URL!**

### Step 5: Configure Environment Variables

For each service, add environment variables:

**Common Variables:**
```
DATABASE_URL=<Internal Database URL>
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Service-Specific:**
- **Content Service:** AWS credentials, S3 bucket
- **Order Service:** Razorpay keys
- **Notification Service:** SendGrid, Twilio keys

### Step 6: Deploy!

Render automatically:
- ✅ Builds your service
- ✅ Deploys
- ✅ Provides public URL (e.g., `https://user-service.onrender.com`)
- ✅ Sets up SSL automatically

**Done! Your API is live!**

---

## 📦 **Using render.yaml (Easier)**

### Option: Deploy All Services at Once

1. **Create `render.yaml`** in root (already created!)
2. **Push to GitHub**
3. **In Render dashboard:**
   - Click **"New +"** → **"Blueprint"**
   - Select repository
   - Render reads `render.yaml` and creates all services!

**Much easier!**

---

## 🔧 **Custom Domain**

### Add Custom Domain:

1. In service dashboard → **"Settings"** → **"Custom Domains"**
2. Add domain (e.g., `api.yourdomain.com`)
3. Render provides DNS records
4. Add DNS records to your domain provider
5. Render auto-configures SSL!

---

## 📊 **Monitoring**

Render provides:
- ✅ Logs (real-time)
- ✅ Metrics (CPU, memory)
- ✅ Deployments history
- ✅ Environment variables management

---

## 💰 **Free Tier Limits**

- ✅ **Free tier** available
- ✅ **750 hours/month** free
- ✅ **PostgreSQL** free (90 days, then $7/month)
- ✅ **SSL** included
- ✅ **Auto-deploy** from Git

**Perfect for MVP and testing!**

---

## ⚠️ **Free Tier Notes**

- **Services sleep after 15 minutes** of inactivity
- **First request** after sleep takes ~30 seconds (cold start)
- **Upgrade to paid** for always-on services

**For production, consider paid plan ($7/month per service)**

---

## 🚀 **Deploy Now!**

1. **Sign up:** https://render.com
2. **Deploy:** Follow steps above
3. **Done!** Your API is live!

**Need help? Check Render docs:** https://render.com/docs

---

## ✅ **Benefits:**

- ✅ **Free tier** - 750 hours/month
- ✅ **Auto-deploy** - Push to GitHub = auto-deploy
- ✅ **PostgreSQL** - Free database
- ✅ **SSL included** - HTTPS automatically
- ✅ **Easy setup** - Simple dashboard
- ✅ **Blueprint** - Deploy all services at once

**Perfect for your platform!**
