# Dermatology AI Assistant Backend

This directory contains the FastAPI backend for the Dermatology AI Assistant.

## Structure

- `app/` - Main application code
  - `api/` - API endpoints
  - `core/` - Core functionality (config, security, logging)
  - `db/` - Database models and CRUD operations
  - `ml/` - Machine learning models and utilities
  - `services/` - Business logic services
  - `schemas/` - Pydantic schemas for validation
  - `utils/` - Utility functions

- `tests/` - Test suite
- `alembic/` - Database migrations
- `main.py` - Application entry point
- `requirements.txt` - Python dependencies

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Setup environment:
```bash
cp ../.env.example ../.env
# Edit .env with your configuration
```

3. Initialize database:
```bash
alembic upgrade head
```

4. Run development server:
```bash
python main.py
```

API docs will be available at http://localhost:8000/api/docs
