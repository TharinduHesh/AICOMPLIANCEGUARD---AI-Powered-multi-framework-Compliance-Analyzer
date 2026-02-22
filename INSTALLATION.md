# 🚀 AIComplianceGuard - Installation & Setup Guide

## Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- Docker & Docker Compose (optional, for containerized deployment)
- Git

## Quick Start (Development)

### 1. Clone Repository

```bash
git clone <repository-url>
cd "ISP Project"
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Create .env file
copy .env.example .env
# Edit .env with your configuration

# Run backend server
uvicorn app.main:app --reload
```

Backend will be available at: `http://localhost:8000`

API Documentation: `http://localhost:8000/api/v1/docs`

### 3. Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Create .env file (optional)
# VITE_API_URL=http://localhost:8000/api/v1

# Run development server
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## Docker Deployment

### Option 1: Docker Compose (Recommended)

```bash
# From project root directory
docker-compose up --build
```

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`

### Option 2: Individual Containers

**Backend:**
```bash
cd backend
docker build -t aicomplianceguard-backend .
docker run -p 8000:8000 --env-file ../.env aicomplianceguard-backend
```

**Frontend:**
```bash
cd frontend
docker build -t aicomplianceguard-frontend .
docker run -p 3000:80 aicomplianceguard-frontend
```

## Configuration

### Backend Configuration (.env)

Key settings in `.env`:

```env
# Application
ENVIRONMENT=development
BACKEND_PORT=8000

# Security
SECRET_KEY=your-secret-key-here
AES_ENCRYPTION_KEY=your-32-byte-key-here
JWT_SECRET=your-jwt-secret-here

# AI/ML
MAX_DOCUMENT_SIZE_MB=10
USE_GPU=false

# Firebase (optional)
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
```

### Frontend Configuration

Create `frontend/.env` (optional):

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## Testing the System

### 1. Test Backend API

```bash
# Health check
curl http://localhost:8000/health

# Get supported frameworks
curl http://localhost:8000/api/v1/compliance/frameworks
```

### 2. Test Frontend

Open browser to `http://localhost:3000`

- Navigate to Dashboard
- Click "Upload Document"
- Upload a sample PDF/DOCX policy document
- Select frameworks and analyze

### 3. Run Backend Tests

```bash
cd backend
pytest tests/ -v --cov
```

## Common Issues & Solutions

### Issue: Module not found

**Solution:**
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Port already in use

**Solution:**
```bash
# Change port in .env
BACKEND_PORT=8001

# Or kill process using port
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

### Issue: Docker build fails

**Solution:**
```bash
# Clean Docker cache
docker system prune -a

# Rebuild
docker-compose build --no-cache
```

## Development Workflow

### Backend Development

```bash
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Run with auto-reload
uvicorn app.main:app --reload --port 8000
```

### Frontend Development

```bash
cd frontend

# Development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Production Deployment

### 1. Environment Setup

- Set `ENVIRONMENT=production` in `.env`
- Use strong secrets for `SECRET_KEY`, `AES_ENCRYPTION_KEY`, `JWT_SECRET`
- Configure Firebase credentials
- Set appropriate `CORS_ORIGINS`

### 2. SSL/TLS Setup

Use a reverse proxy (nginx/Apache) with SSL certificates:

```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:3000;
    }

    location /api {
        proxy_pass http://localhost:8000;
    }
}
```

### 3. Database Setup

- Configure Firebase Firestore
- Set up Firebase Authentication
- Create necessary indexes

### 4. Monitoring

- Set up logging aggregation
- Configure health check endpoints
- Enable error tracking (Sentry)

## Maintenance

### Update Dependencies

**Backend:**
```bash
pip install --upgrade -r requirements.txt
```

**Frontend:**
```bash
npm update
```

### Cleanup Temporary Files

```bash
# Via API
curl -X POST http://localhost:8000/api/v1/admin/cleanup

# Manual
rm -rf backend/temp_uploads/*
rm -rf backend/logs/*
```

### Backup

- Backup Firebase Firestore data
- Backup framework data files
- Backup trained ML models

## Support

For issues, questions, or feature requests:

- Check documentation in `docs/` folder
- Review API documentation at `/api/v1/docs`
- Contact: [Your Contact Information]

## Next Steps

After installation:

1. ✅ Test document upload
2. ✅ Run sample compliance analysis
3. ✅ Review CIA balance analysis
4. ✅ Check audit risk prediction
5. ✅ Explore framework mappings

---

**Built with ❤️ for secure compliance automation**
