# 🚀 AIComplianceGuard - Quick Start Guide

## Prerequisites Check

You have:
- ✅ Python 3.13.7 installed (use `py` command)
- ❌ Docker not installed
- ✅ Virtual environment created at `backend\venv`

## Option 1: Let Dependencies Install (Recommended)

The installation was started but cancelled. Please continue:

```powershell
# 1. Activate virtual environment
& "C:\Users\ranas\Desktop\ISP Project\backend\venv\Scripts\Activate.ps1"

# 2. Install dependencies (this will take 10-15 minutes with slow network)
pip install -r backend\requirements.txt

# 3. Download spaCy language model
python -m spacy download en_core_web_sm

# 4. Create .env file
Copy-Item .env.example backend\.env

# 5. Start backend server
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Then in a NEW PowerShell terminal:**

```powershell
# 6. Install frontend dependencies
cd "C:\Users\ranas\Desktop\ISP Project\frontend"
npm install

# 7. Start frontend dev server (optional if you want UI)
npm run dev
```

Access:
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/v1/docs
- Frontend: http://localhost:3000 (if you ran npm run dev)

---

## Option 2: Minimal Backend-Only Demo (5 minutes)

If you want to test quickly without waiting for full installation:

```powershell
# 1. Activate venv
& "C:\Users\ranas\Desktop\ISP Project\backend\venv\Scripts\Activate.ps1"

# 2. Install only core dependencies (much faster)
pip install fastapi uvicorn python-dotenv pydantic

# 3. Create minimal .env
@"
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ENCRYPTION_KEY=your-32-character-encryption-key-here-change-this
"@ | Out-File -FilePath "backend\.env" -Encoding utf8

# 4. Start minimal API
cd backend
uvicorn app.main:app --reload --port 8000
```

This will start the API framework, though some features requiring ML/NLP libraries won't work until full installation completes.

---

## Option 3: Install Docker Desktop (for future use)

If you want to use Docker later:

1. Download: https://www.docker.com/products/docker-desktop/
2. Install Docker Desktop for Windows
3. Restart your computer
4. Then run: `docker compose up --build` (note: no hyphen in newer Docker)

---

## Troubleshooting

### Slow pip install?
- The installation is downloading ~500MB of packages
- Pillow (46MB) needs to compile from source
- Consider running overnight or with better internet

### "Execution policy" error when activating venv?
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Missing build tools for Pillow?
- Install Microsoft C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Or wait for pre-built wheel to download

### Node.js not installed (for frontend)?
- Download: https://nodejs.org/ (LTS version)
- Install and restart PowerShell
- Then run `npm install` in frontend directory

---

## What to Do Next

**Immediate:**
1. Let the pip installation complete (Option 1)
2. Or do minimal test (Option 2)
3. Check API docs at http://localhost:8000/api/v1/docs

**Once Backend is Running:**
1. Upload a PDF/DOCX compliance document via API docs
2. Call the `/api/v1/compliance/analyze` endpoint
3. See AI-powered analysis results

**For Full Experience:**
1. Install Node.js if you want the React frontend
2. Or install Docker Desktop for containerized deployment
3. Configure Firebase credentials for database (optional for testing)

---

## Current Installation Status

✅ Python virtual environment created  
🔄 Dependencies installing (cancelled at 59% - need to restart)  
❌ spaCy model not downloaded yet  
❌ Frontend dependencies not installed yet  
❌ Docker not available  

---

## Quick Test Without Full Installation

You can test the system architecture without ML features:

1. View the comprehensive documentation:
   - [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Complete overview
   - [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Technical details
   - [docs/API.md](docs/API.md) - API reference

2. Explore the code:
   - `backend/app/modules/` - All 7 core modules
   - `backend/app/api/endpoints/` - API endpoints
   - `frontend/src/pages/` - React components
   - `data/frameworks/` - Compliance framework data (275+ controls)

3. Review the Novel Research Contribution:
   - CIA Balance Index formula in `backend/app/modules/cia_validator/validator.py`
   - Implementation details in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## Time Estimates

| Task | Time |
|------|------|
| Full pip install | 10-15 min (slow network) |
| spaCy model download | 2-3 min |
| Frontend npm install | 5-10 min |
| Docker Desktop install | 15-20 min + restart |
| Manual Python setup | 1 min |
| Reading documentation | 30 min |

---

## Need Help?

1. Check INSTALLATION.md for detailed setup instructions
2. See troubleshooting section in that file
3. Review error messages carefully - most are dependency-related

**Your system is complete and ready - just needs dependencies installed!** 🎉
