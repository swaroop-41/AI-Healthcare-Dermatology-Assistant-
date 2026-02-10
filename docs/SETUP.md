# Setup Guide

## Prerequisites

### System Requirements
- **OS**: Linux, macOS, or Windows 10+
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB free space
- **Python**: 3.10 or higher
- **Node.js**: 18.0 or higher
- **PostgreSQL**: 16.0 or higher

### Optional
- Docker Desktop (for containerized deployment)
- CUDA-capable GPU (for faster model inference)

## Local Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/swaroop-41/AI-Healthcare-Dermatology-Assistant-.git
cd AI-Healthcare-Dermatology-Assistant-
```

### 2. Database Setup

#### Install PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**macOS (with Homebrew):**
```bash
brew install postgresql@16
brew services start postgresql@16
```

**Windows:**
Download and install from [postgresql.org](https://www.postgresql.org/download/windows/)

#### Create Database

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE dermatology_db;
CREATE USER admin WITH ENCRYPTED PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE dermatology_db TO admin;
\q
```

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Configure environment
cd ..
cp .env.example .env

# Edit .env with your settings
nano .env  # or use your preferred editor
```

#### Configure .env File

Update the following critical settings:

```bash
# Database
DATABASE_URL=postgresql://admin:your_password@localhost:5432/dermatology_db

# Security (generate strong random keys)
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Paths
MODEL_PATH=./models/skin_multiclass.pth

# Optional: OpenAI API (for chatbot)
OPENAI_API_KEY=your-openai-api-key
```

#### Initialize Database Tables

```bash
cd backend
python -c "from app.db.base import init_db; init_db()"
```

#### Run Backend

```bash
python main.py
```

Backend will be available at: http://localhost:8000  
API Docs: http://localhost:8000/api/docs

### 4. Frontend Setup

```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# Configure API URL (optional - defaults to localhost:8000)
# Create .env.local file
echo "VITE_API_URL=http://localhost:8000/api/v1" > .env.local

# Start development server
npm run dev
```

Frontend will be available at: http://localhost:3000

### 5. Model Setup

Place your trained model file at:
```
models/skin_multiclass.pth
```

If you don't have a trained model, the system will use an untrained placeholder (predictions won't be accurate until you train or provide a model).

## Docker Deployment

### 1. Install Docker

Follow instructions at [docs.docker.com](https://docs.docker.com/get-docker/)

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with production settings
```

### 3. Build and Run

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- PostgreSQL: localhost:5432

## Verification

### Test Backend

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Dermatology AI Assistant",
  "version": "1.0.0"
}
```

### Test Frontend

Open http://localhost:3000 in your browser. You should see the login page.

### Create First User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123",
    "full_name": "Test User",
    "role": "patient"
  }'
```

## Troubleshooting

### Backend Issues

**Database connection error:**
- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check DATABASE_URL in .env
- Ensure database exists and credentials are correct

**Import errors:**
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

**Model not found:**
- Place model file at `models/skin_multiclass.pth`
- Or train a new model (see training documentation)

### Frontend Issues

**npm install fails:**
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and try again

**API connection error:**
- Verify backend is running on port 8000
- Check CORS settings in backend config
- Verify VITE_API_URL in .env.local

### Docker Issues

**Build fails:**
- Ensure Docker daemon is running
- Check docker-compose.yml syntax
- Verify .env file exists

**Container crashes:**
- Check logs: `docker-compose logs [service-name]`
- Verify environment variables
- Ensure ports are not already in use

## Next Steps

1. **Train Model**: See [training/README.md](../training/README.md)
2. **Add Data**: Import patient records via API
3. **Configure Security**: Update SECRET_KEY and JWT_SECRET_KEY
4. **Setup Monitoring**: Configure logging and metrics
5. **Production Deploy**: See [DEPLOYMENT.md](DEPLOYMENT.md)

## Development Workflow

```bash
# Backend changes
cd backend
python main.py  # Auto-reloads on file changes

# Frontend changes
cd frontend
npm run dev  # Hot reload enabled

# Run tests
cd backend
pytest tests/

# Build for production
cd frontend
npm run build
```

## Support

For issues:
- Check existing documentation
- Search GitHub issues
- Create new issue with details

Happy developing! 🚀
