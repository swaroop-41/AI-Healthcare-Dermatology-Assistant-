# 🏥 AI Healthcare Dermatology Assistant

A production-ready **Multi-Modal AI Healthcare Assistant** specialized in Dermatology with enterprise-grade features, security, and user experience.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![React](https://img.shields.io/badge/react-18.2-blue)

## ✨ Features

### 🔬 Advanced AI Dermatology Analysis
- **ResNet18-based Classifier**: 86% accuracy on ISIC dataset
- **8 Skin Condition Classes**: AK, BCC, BKL, DF, MEL, NV, SCC, VASC
- **Grad-CAM++ Visualization**: Explainable AI with attention heatmaps
- **ABCDE Rule Analysis**: Automated melanoma risk assessment
- **Fitzpatrick Skin Tone Classification**: Types I-VI
- **Lesion Measurement**: Automated diameter estimation

### 🧠 Medical-Grade NLP
- BioBERT-based symptom extraction
- Medical Named Entity Recognition (NER)
- Symptom severity classification
- Rule-based medical Q&A chatbot (GPT integration ready)

### 🗄️ Comprehensive Data Management
- **PostgreSQL Database**: Patient records, diagnoses, medical images
- **CRUD Operations**: Full patient and diagnosis management
- **Image Comparison**: Track lesion changes over time
- **Audit Logging**: HIPAA-compliant access tracking

### 📊 Risk Assessment
- Multi-modal risk prediction
- Patient demographics integration
- Family history analysis
- ABCDE score-based melanoma risk
- Personalized recommendations

### 📄 Professional Reporting
- Hospital-grade PDF reports (ReportLab)
- Grad-CAM visualization included
- Patient demographics and medical history
- Clinical recommendations

### 🔒 Enterprise Security
- JWT token authentication
- Bcrypt password hashing
- Role-based access control (Patient, Doctor, Admin)
- OAuth2 password flow
- HIPAA-compliant data handling

### 📈 Admin Dashboard
- System analytics and statistics
- Model performance metrics
- User activity tracking
- System health monitoring

### 🎨 Professional React Frontend
- Modern, responsive UI with TailwindCSS
- Image upload with drag-and-drop
- Interactive Grad-CAM viewer
- Patient dashboard with history
- Real-time analysis results
- PDF report download

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 16
- Docker & Docker Compose (optional)

### Option 1: Docker Deployment (Recommended)

```bash
# Clone repository
git clone https://github.com/swaroop-41/AI-Healthcare-Dermatology-Assistant-.git
cd AI-Healthcare-Dermatology-Assistant-

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

### Option 2: Local Development

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp ../.env.example ../.env
# Edit .env with your configuration

# Initialize database (PostgreSQL must be running)
createdb dermatology_db

# Run the application
python main.py
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## ⚕️ Medical Disclaimer

**IMPORTANT**: This AI system is designed to **ASSIST** healthcare professionals, not replace them. 

- ❌ NOT FDA approved for clinical diagnosis
- ✅ For research and educational purposes
- ✅ All diagnoses should be reviewed by qualified dermatologists
- ✅ Consult licensed medical professionals for clinical decisions

## 🛠️ Tech Stack

**Backend:**
- FastAPI 0.109.1 (security patched)
- PyTorch 2.6.0 (security patched)
- PostgreSQL 16
- SQLAlchemy 2.0
- ReportLab 4.0
- WeasyPrint 68.0 (security patched)

**Frontend:**
- React 18.2
- TailwindCSS 3.4
- Vite 5.0
- Axios
- React Router 6

**ML/AI:**
- PyTorch 2.6.0 & TorchVision 0.21.0 (security patched)
- Transformers 4.48.0 (security patched)
- OpenCV
- Pillow 10.3.0 (security patched)
- scikit-learn

**DevOps:**
- Docker & Docker Compose
- Nginx
- PostgreSQL
- Redis

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please read the documentation for guidelines.

---

**Built with ❤️ for better dermatological care**