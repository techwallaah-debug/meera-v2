# ✅ Hostinger Deployment Checklist

## Complete step-by-step checklist

---

## 📋 Pre-Deployment

- [ ] Hostinger VPS purchased
- [ ] VPS IP address noted
- [ ] SSH access configured
- [ ] Domain name ready
- [ ] API keys collected (Razorpay, SendGrid, etc.)

---

## 🚀 Step 1: Upload Project

### Choose upload method:

- [ ] **Option A: Git** (Recommended)
  ```bash
  # On VPS
  cd /opt
  git clone <repo-url> social-commerce
  ```

- [ ] **Option B: SFTP** (FileZilla/WinSCP)
  - [ ] Connected via SFTP
  - [ ] Uploaded project to `/opt/social-commerce`
  - [ ] Verified files uploaded

- [ ] **Option C: SCP**
  ```bash
  scp -r Meera root@vps-ip:/opt/social-commerce
  ```

**Verification:**
```bash
cd /opt/social-commerce
ls -la
# Should see: backend, frontend, infrastructure, etc.
```

---

## 🔧 Step 2: Run Deployment Script

- [ ] Navigated to deployment directory
  ```bash
  cd /opt/social-commerce/infrastructure/hostinger
  ```

- [ ] Made scripts executable
  ```bash
  chmod +x scripts/*.sh
  ```

- [ ] Ran deployment script
  ```bash
  sudo ./scripts/deploy-hostinger.sh
  ```

- [ ] Script completed successfully
- [ ] Docker installed
- [ ] Docker Compose installed
- [ ] `.env` file created
- [ ] All services started

**If script fails:**
- [ ] Check logs: `docker-compose logs`
- [ ] Verify Docker: `docker --version`
- [ ] Check disk space: `df -h`
- [ ] Check memory: `free -h`

---

## ⚙️ Step 3: Configure Environment

- [ ] Edited `.env` file
  ```bash
  nano .env
  ```

- [ ] Set database passwords
- [ ] Set JWT secret key
- [ ] Added Razorpay keys
- [ ] Added SendGrid key
- [ ] Added Twilio credentials (optional)
- [ ] Saved `.env` file

**Required variables:**
- [ ] `DB_PASSWORD` - Strong password
- [ ] `MYSQL_ROOT_PASSWORD` - Strong password
- [ ] `JWT_SECRET_KEY` - Long random string (64+ chars)
- [ ] `RAZORPAY_KEY_ID` - Your Razorpay key
- [ ] `RAZORPAY_KEY_SECRET` - Your Razorpay secret

---

## 🌐 Step 4: Configure Domain DNS

- [ ] Logged into Hostinger hPanel
- [ ] Navigated to DNS settings
- [ ] Added A record:
  - [ ] Type: A
  - [ ] Name: `api` (or your subdomain)
  - [ ] Points to: [Your VPS IP]
  - [ ] TTL: 3600
- [ ] Saved DNS record
- [ ] Waited for DNS propagation (5-30 min)

**Verify DNS:**
```bash
# On your local machine
nslookup api.yourdomain.com
# Should return your VPS IP
```

**Or use helper script:**
```bash
./scripts/setup-dns-guide.sh
```

---

## 🔒 Step 5: Setup SSL Certificate

- [ ] Domain DNS propagated
- [ ] Domain resolves to VPS IP
- [ ] Ran SSL setup script
  ```bash
  ./scripts/setup-ssl.sh api.yourdomain.com your@email.com
  ```

- [ ] SSL certificate generated
- [ ] Certificates copied to `nginx/ssl/`
- [ ] Updated nginx config with domain
- [ ] Restarted nginx
  ```bash
  docker-compose -f docker-compose.hostinger.yml restart nginx
  ```

**Verify SSL:**
```bash
curl https://api.yourdomain.com/health
```

**Setup auto-renewal:**
```bash
crontab -e
# Add: 0 0 * * * certbot renew --quiet && cd /opt/social-commerce/infrastructure/hostinger && docker-compose -f docker-compose.hostinger.yml restart nginx
```

---

## 🧪 Step 6: Test API

- [ ] Tested health endpoint
  ```bash
  curl https://api.yourdomain.com/health
  ```

- [ ] Tested user service
  ```bash
  curl https://api.yourdomain.com/users/health
  ```

- [ ] Tested registration
  ```bash
  curl -X POST https://api.yourdomain.com/users/register \
    -H "Content-Type: application/json" \
    -d '{"email":"test@example.com","username":"test","full_name":"Test","password":"test123"}'
  ```

- [ ] Tested product service
  ```bash
  curl https://api.yourdomain.com/products
  ```

**Or use test script:**
```bash
./scripts/test-api.sh api.yourdomain.com
```

**Verify deployment:**
```bash
./scripts/verify-deployment.sh api.yourdomain.com
```

---

## 🔍 Post-Deployment Verification

- [ ] All containers running
  ```bash
  docker-compose -f docker-compose.hostinger.yml ps
  ```

- [ ] Services healthy
  ```bash
  docker-compose -f docker-compose.hostinger.yml logs | grep -i error
  ```

- [ ] Database accessible
  ```bash
  docker exec mysql mysql -u admin -p -e "SHOW DATABASES;"
  ```

- [ ] Redis working
  ```bash
  docker exec redis redis-cli ping
  ```

- [ ] Nginx serving requests
  ```bash
  curl -I https://api.yourdomain.com/health
  ```

- [ ] SSL certificate valid
  ```bash
  echo | openssl s_client -connect api.yourdomain.com:443 -servername api.yourdomain.com 2>/dev/null | openssl x509 -noout -dates
  ```

---

## 🔐 Security Checklist

- [ ] Firewall configured (UFW)
  ```bash
  ufw allow 22/tcp
  ufw allow 80/tcp
  ufw allow 443/tcp
  ufw enable
  ```

- [ ] Strong passwords set in `.env`
- [ ] SSH secured (key-based auth recommended)
- [ ] SSL certificate installed
- [ ] Rate limiting enabled (in nginx)
- [ ] Regular backups scheduled

---

## 📊 Monitoring Setup

- [ ] Logs accessible
  ```bash
  docker-compose -f docker-compose.hostinger.yml logs -f
  ```

- [ ] Resource monitoring
  ```bash
  docker stats
  ```

- [ ] Backup script tested
  ```bash
  ./scripts/backup.sh
  ```

---

## ✅ Final Checks

- [ ] API accessible from internet
- [ ] SSL working (HTTPS)
- [ ] All endpoints responding
- [ ] Mobile app can connect
- [ ] Admin dashboard accessible (if deployed)
- [ ] Backups working
- [ ] Monitoring set up

---

## 🎉 **Deployment Complete!**

**Your API is live at:**
- `https://api.yourdomain.com`

**Useful Commands:**
```bash
# View logs
docker-compose -f docker-compose.hostinger.yml logs -f

# Restart services
docker-compose -f docker-compose.hostinger.yml restart

# Backup
./scripts/backup.sh

# Test API
./scripts/test-api.sh api.yourdomain.com
```

---

**🚀 Platform is live on Hostinger!**
