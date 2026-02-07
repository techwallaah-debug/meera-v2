# 🏠 Local Deployment Guide - Test Before Deploying

## ✅ **Test Everything Locally First!**

Perfect for testing before deploying to Hostinger VPS.

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Start Infrastructure

```bash
# Start MySQL, Redis, Elasticsearch
docker-compose up -d

# Verify they're running
docker-compose ps
```

### Step 2: Setup Python Environment

```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit if needed (defaults work for local)
nano .env
```

### Step 4: Start Services

**Option A: Use Script (Easiest)**
```bash
./scripts/start-all-services.sh
```

**Option B: Manual (Separate Terminals)**

**Terminal 1 - User Service:**
```bash
cd backend/services/user-service/src
python main.py
```

**Terminal 2 - Content Service:**
```bash
cd backend/services/content-service/src
python main.py
```

**Terminal 3 - Product Service:**
```bash
cd backend/services/product-service/src
python main.py
```

**Terminal 4 - Order Service:**
```bash
cd backend/services/order-service/src
python main.py
```

### Step 5: Test APIs

```bash
# Health checks
curl http://localhost:8001/health  # User Service
curl http://localhost:8002/health  # Content Service
curl http://localhost:8003/health  # Product Service
curl http://localhost:8004/health  # Order Service

# API Documentation
# Open in browser:
# http://localhost:8001/docs
# http://localhost:8002/docs
# http://localhost:8003/docs
# http://localhost:8004/docs
```

---

## 📱 Connect Mobile App to Local Server

### Option 1: Same Network (WiFi)

**1. Find your local IP:**
```bash
# Mac/Linux
ifconfig | grep "inet " | grep -v 127.0.0.1

# Windows
ipconfig
```

**2. Update mobile app:**
```typescript
// frontend/mobile/src/services/api.ts
const API_BASE_URL = 'http://YOUR_LOCAL_IP:8001';
// Example: http://192.168.1.100:8001
```

**3. Run mobile app:**
```bash
cd frontend/mobile
npm install
npm start
# Then run on iOS/Android
```

### Option 2: Use ngrok (External Access)

**1. Install ngrok:**
- Download from https://ngrok.com
- Or: `brew install ngrok` (Mac)

**2. Expose local server:**
```bash
# Expose User Service
ngrok http 8001

# You'll get: https://abc123.ngrok.io
```

**3. Update mobile app:**
```typescript
const API_BASE_URL = 'https://abc123.ngrok.io';
```

**Benefits:**
- ✅ Works from anywhere
- ✅ HTTPS included
- ✅ Easy to test on real device

---

## 🧪 Test Complete Flow Locally

### 1. Register User
```bash
curl -X POST http://localhost:8001/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "full_name": "Test User",
    "password": "testpass123"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8001/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpass123"
```

### 3. Create Product
```bash
# Get token from login response first
TOKEN="your-token-here"

curl -X POST http://localhost:8003/products \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Product",
    "category": "fashion",
    "price": 999.99,
    "image_urls": [],
    "stock_quantity": 10,
    "sku": "TEST-001"
  }'
```

### 4. Add to Cart
```bash
curl -X POST http://localhost:8004/cart \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 1
  }'
```

---

## 🔧 Troubleshooting Local Setup

### Port Already in Use

```bash
# Find what's using the port
lsof -i :8001  # Mac/Linux
netstat -ano | findstr :8001  # Windows

# Kill the process or change port in service
```

### Database Connection Failed

```bash
# Check MySQL is running
docker-compose ps mysql

# Check connection
docker exec mysql mysql -u admin -p
# Password: password (from .env)
```

### Services Not Starting

```bash
# Check logs
docker-compose logs

# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install --upgrade -r backend/requirements.txt
```

---

## 📊 Local Development Benefits

- ✅ **Fast iteration** - Changes reflect immediately
- ✅ **Easy debugging** - See logs in real-time
- ✅ **No costs** - Run on your machine
- ✅ **Test before deploy** - Catch issues early
- ✅ **Full control** - Modify anything easily

---

## 🎯 Next Steps After Local Testing

**Once everything works locally:**

1. ✅ Deploy to Hostinger VPS
2. ✅ Update mobile app API URL
3. ✅ Test on production
4. ✅ Go live!

---

## 🚀 **Start Local Testing Now!**

```bash
# 1. Start infrastructure
docker-compose up -d

# 2. Start services
./scripts/start-all-services.sh

# 3. Test
curl http://localhost:8001/health
```

**✅ Everything works locally? Then deploy to Hostinger!**
