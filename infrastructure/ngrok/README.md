# 🌐 ngrok Setup Guide - Expose Local Server

## ✅ **100% Free - Expose Your Local Server to Internet!**

Perfect for testing your mobile app with local backend!

---

## 🚀 **Quick Setup (5 Minutes)**

### Step 1: Install ngrok

**Mac:**
```bash
brew install ngrok
```

**Linux:**
```bash
# Download from https://ngrok.com/download
# Or use snap
snap install ngrok
```

**Windows:**
- Download from https://ngrok.com/download
- Extract and add to PATH

### Step 2: Sign Up (Free)

1. Go to https://ngrok.com
2. Sign up (free)
3. Get your auth token from dashboard

### Step 3: Authenticate

```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

### Step 4: Start Your Local Services

```bash
# Start infrastructure
docker-compose up -d

# Start services (in separate terminals)
cd backend/services/user-service/src && python main.py
cd backend/services/content-service/src && python main.py
# ... etc
```

### Step 5: Expose with ngrok

**Terminal 1 - User Service:**
```bash
ngrok http 8001
```

**Terminal 2 - Content Service:**
```bash
ngrok http 8002
```

**Terminal 3 - Product Service:**
```bash
ngrok http 8003
```

**Terminal 4 - Order Service:**
```bash
ngrok http 8004
```

### Step 6: Get Public URLs

ngrok will show:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8001
```

**Use these URLs in your mobile app!**

---

## 📱 **Update Mobile App**

```typescript
// frontend/mobile/src/services/api.ts

// Option 1: Use ngrok URLs directly
const API_BASE_URL = 'https://abc123.ngrok.io';

// Option 2: Use environment variable
const API_BASE_URL = process.env.API_BASE_URL || 'https://abc123.ngrok.io';
```

---

## 🔧 **Multiple Services Setup**

### Option 1: Separate ngrok Instances (Recommended)

Run ngrok for each service in separate terminals:
- User Service: `ngrok http 8001`
- Content Service: `ngrok http 8002`
- Product Service: `ngrok http 8003`
- Order Service: `ngrok http 8004`

**Each gets its own URL!**

### Option 2: ngrok Config File

Create `ngrok.yml`:
```yaml
version: "2"
authtoken: YOUR_AUTH_TOKEN

tunnels:
  user-service:
    addr: 8001
    proto: http
  content-service:
    addr: 8002
    proto: http
  product-service:
    addr: 8003
    proto: http
  order-service:
    addr: 8004
    proto: http
```

Start all:
```bash
ngrok start --all
```

---

## 🎯 **Static Domain (Free Tier)**

### Get Free Static Domain:

1. Go to ngrok dashboard
2. Click "Your Domains"
3. Click "Create Domain"
4. Choose free domain (e.g., `your-app.ngrok-free.app`)
5. Use in config:

```yaml
tunnels:
  user-service:
    addr: 8001
    proto: http
    domain: your-app.ngrok-free.app
```

**Now you have a permanent URL!**

---

## 💰 **Free Tier Limits**

- ✅ **Free forever**
- ✅ **1 tunnel** at a time (free tier)
- ✅ **40 connections/minute** limit
- ✅ **HTTPS included**
- ✅ **Static domain** available

**Perfect for testing!**

---

## 🚀 **Quick Start Script**

Create `scripts/start-with-ngrok.sh`:

```bash
#!/bin/bash

# Start services
./scripts/start-local.sh

# Start ngrok
echo "Starting ngrok..."
ngrok http 8001

# Show URL
echo "Your API is available at:"
echo "Check ngrok dashboard: http://127.0.0.1:4040"
```

---

## 📊 **ngrok Dashboard**

Access local dashboard:
```
http://127.0.0.1:4040
```

**Features:**
- ✅ View requests
- ✅ Replay requests
- ✅ Inspect headers
- ✅ View logs

---

## ✅ **Benefits:**

- ✅ **100% free** - Forever
- ✅ **HTTPS included** - Secure
- ✅ **Easy setup** - 5 minutes
- ✅ **Perfect for testing** - Mobile app can access
- ✅ **No server needed** - Run locally

**Perfect for development and testing!**

---

## 🎯 **Use Cases:**

- ✅ **Mobile app testing** - Test with real device
- ✅ **Webhook testing** - Receive webhooks locally
- ✅ **API testing** - Share API with team
- ✅ **Development** - Fast iteration

---

## 🚀 **Start Now!**

```bash
# 1. Install ngrok
brew install ngrok

# 2. Authenticate
ngrok config add-authtoken YOUR_TOKEN

# 3. Start services
./scripts/start-local.sh

# 4. Expose
ngrok http 8001
```

**Done! Your local server is now public!**
