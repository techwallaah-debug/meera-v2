# AI-Powered Social Commerce Platform 🚀

India's most advanced social commerce platform - combining social media with e-commerce powered by AI.

## 🎯 Project Overview

This platform enables users to:
- Share content (posts, stories) with product tags
- Discover products through social feeds
- Purchase products directly from posts
- Get AI-powered personalized recommendations
- Visual search for products
- Follow creators and shop their recommendations

## 🚀 Deployment Options (No Server Needed!)

**✅ Deploy for FREE - Multiple Options Available!**

- **🥇 Railway.app** (Recommended) - 500 hours/month free, auto-deploy from GitHub
  - Guide: [`infrastructure/railway/README.md`](infrastructure/railway/README.md)
- **🥈 Render.com** - Free tier, easy setup
  - Guide: [`infrastructure/render/README.md`](infrastructure/render/README.md)
- **🥉 Local + ngrok** - 100% free forever, perfect for testing
  - Guide: [`infrastructure/ngrok/README.md`](infrastructure/ngrok/README.md)

**📖 See [`START_HERE.md`](START_HERE.md) for quick start guide!**

---

## 🏗️ Architecture

- **Backend**: Microservices architecture with FastAPI (Python)
- **Database**: MySQL 8.0 (Primary), Redis (Cache), Elasticsearch (Search), Pinecone (Vectors)
- **Frontend**: React Native (Mobile), Next.js (Web)
- **AI/ML**: PyTorch, OpenAI GPT-4, Custom recommendation models
- **Infrastructure**: Docker, Kubernetes (or free hosting like Railway/Render)

## 📋 Prerequisites

- Node.js 20 LTS
- Python 3.11+
- Docker & Docker Compose
- MySQL 8.0 (via Docker)
- Redis 7 (via Docker)
- Git
- Cursor IDE (with AI enabled)

## 🚀 Quick Start

### Option A: Deploy to Free Hosting (Recommended)

**Railway (Easiest):**
1. Sign up at https://railway.app
2. Deploy from GitHub
3. Add database
4. Done! See [`infrastructure/railway/README.md`](infrastructure/railway/README.md)

**Render:**
1. Sign up at https://render.com
2. Create web service
3. Connect GitHub
4. Deploy! See [`infrastructure/render/README.md`](infrastructure/render/README.md)

### Option B: Local Development

**Quick Start Script:**
```bash
./scripts/start-local.sh
```

**Manual Setup:**

1. **Clone the Repository**
```bash
git clone <repository-url>
cd Meera
```

2. **Set Up Environment Variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start Infrastructure Services**
```bash
docker-compose up -d
```

This starts:
- MySQL (port 3306)
- Redis (port 6379)
- Elasticsearch (port 9200)
- Mailhog (port 8025 for email testing)

4. **Set Up Python Backend**
```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt
```

5. **Run Services**

#### User Service (Port 8001)
```bash
cd backend/services/user-service/src
python main.py
```

#### Content Service (Port 8002)
```bash
cd backend/services/content-service/src
python main.py
```

#### Product Service (Port 8003)
```bash
cd backend/services/product-service/src
python main.py
```

6. **Access Services**

- User Service API: http://localhost:8001/docs
- Content Service API: http://localhost:8002/docs
- Product Service API: http://localhost:8003/docs
- Mailhog UI: http://localhost:8025

### Option C: Local + ngrok (For Mobile Testing)

```bash
# 1. Start services locally
./scripts/start-local.sh

# 2. Expose with ngrok
ngrok http 8001

# 3. Use ngrok URL in mobile app
```

See [`infrastructure/ngrok/README.md`](infrastructure/ngrok/README.md) for details.

## 📁 Project Structure

```
Meera/
├── backend/
│   ├── services/          # Microservices
│   │   ├── user-service/
│   │   ├── content-service/
│   │   ├── product-service/
│   │   └── ...
│   ├── shared/            # Shared utilities
│   │   ├── database/
│   │   ├── auth/
│   │   └── utils/
│   └── ml/                # ML models and training
├── frontend/
│   ├── mobile/            # React Native app
│   └── web/               # Next.js web app
├── infrastructure/        # Docker, K8s, Terraform
├── docs/                  # Documentation
└── tests/                 # Test suites
```

## 🔧 Development

### Database Migrations

We're using SQLAlchemy with Alembic for migrations (to be set up).

### Testing

```bash
# Run tests
pytest tests/
```

### Code Style

- Python: Follow PEP 8
- Use type hints
- Document functions with docstrings

## 📚 API Documentation

Each service provides interactive API documentation via Swagger UI:
- Navigate to `http://localhost:<port>/docs` for any service

## 🔐 Authentication

The platform uses JWT tokens for authentication:
1. Register: `POST /register`
2. Login: `POST /token`
3. Use token: `Authorization: Bearer <token>`

## 🛠️ Tech Stack

### Backend
- FastAPI 0.109
- SQLAlchemy 2.0
- MySQL 8.0
- Redis 7.2
- Elasticsearch 8.11

### Frontend (Coming Soon)
- React Native 0.73
- Next.js 14
- TypeScript 5.3

### AI/ML (Coming Soon)
- PyTorch 2.1
- OpenAI GPT-4
- Sentence Transformers
- Custom recommendation models

## 📝 Environment Variables

See `.env.example` for all required environment variables.

Key variables:
- `DATABASE_URL`: MySQL connection string
- `REDIS_URL`: Redis connection string
- `JWT_SECRET_KEY`: Secret for JWT tokens
- `AWS_ACCESS_KEY_ID`: AWS credentials for S3
- `OPENAI_API_KEY`: OpenAI API key

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Write tests
4. Submit a pull request

## 📄 License

[Your License Here]

## 🎯 Roadmap

- [x] Project structure setup
- [x] User Service (MySQL)
- [x] Content Service
- [x] Product Service
- [ ] Order Service
- [ ] Search Service (Elasticsearch)
- [ ] Recommendation Service
- [ ] Frontend (React Native)
- [ ] Frontend (Next.js)
- [ ] AI/ML Models
- [ ] Deployment (Kubernetes)

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

**Built with ❤️ for India's Social Commerce Revolution**
