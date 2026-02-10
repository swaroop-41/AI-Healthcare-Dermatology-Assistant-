# API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <access_token>
```

## Endpoints

### Authentication

#### Register User
```http
POST /auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "full_name": "John Doe",
  "role": "patient"  // Options: patient, doctor, admin
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "patient",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00"
}
```

#### Login
```http
POST /auth/login
```

**Request Body:** (Form Data)
```
username=user@example.com&password=SecurePass123
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### Get Current User
```http
GET /auth/me
```

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "patient",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00"
}
```

#### Logout
```http
POST /auth/logout
```

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "message": "Successfully logged out"
}
```

---

### Dermatology Analysis

#### Analyze Skin Lesion
```http
POST /dermatology/analyze
```

**Headers:** `Authorization: Bearer <token>`

**Request Body:** (Multipart Form Data)
```
file: <image file>
body_location: "arm" (optional)
```

**Response:** `200 OK`
```json
{
  "diagnosis": {
    "primary_prediction": "MEL",
    "confidence": 0.87,
    "all_predictions": [
      {"class": "MEL", "name": "Melanoma", "confidence": 0.87},
      {"class": "NV", "name": "Melanocytic Nevus", "confidence": 0.08},
      {"class": "BCC", "name": "Basal Cell Carcinoma", "confidence": 0.03}
    ],
    "ensemble_consensus": null
  },
  "clinical_analysis": {
    "abcde_score": {
      "asymmetry": 0.7,
      "border": 0.6,
      "color": 0.8,
      "diameter_mm": 6.2,
      "evolution": "unknown"
    },
    "skin_tone": "Type III (Fitzpatrick)",
    "body_location": "arm"
  },
  "visualization": {
    "gradcam_path": "/heatmaps/gradcam_abc123.jpg",
    "segmentation_mask": null
  },
  "risk_assessment": {
    "overall_risk": "high",
    "melanoma_risk_score": 0.78,
    "risk_factors": [
      "AI detected melanoma (confidence: 87%)",
      "High asymmetry score",
      "Irregular border detected",
      "Lesion diameter > 6mm (6.2mm)"
    ],
    "protective_factors": [],
    "recommendation": "Urgent dermatologist consultation recommended within 2 weeks."
  },
  "recommendation": "Urgent dermatologist consultation recommended within 2 weeks."
}
```

#### Get Patient Diagnoses
```http
GET /dermatology/diagnoses
```

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
[
  {
    "id": "uuid",
    "patient_id": "uuid",
    "image_id": "uuid",
    "primary_prediction": "MEL",
    "confidence_score": 0.87,
    "all_predictions": [...],
    "risk_level": "high",
    "recommendation": "Urgent consultation recommended",
    "status": "pending_review",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

#### Get Specific Diagnosis
```http
GET /dermatology/diagnoses/{diagnosis_id}
```

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK` (Same structure as individual diagnosis above)

---

### Patient Management

#### Create/Update Patient Profile
```http
POST /patients/profile
```

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "date_of_birth": "1990-01-01",
  "gender": "male",
  "skin_type": "Type III",
  "phone_number": "+1234567890",
  "address": "123 Main St",
  "medical_history": {
    "smoking": false,
    "regular_skin_checks": true
  },
  "family_history": {
    "melanoma": false,
    "skin_cancer": false
  },
  "allergies": ["penicillin"]
}
```

**Response:** `201 Created` or `200 OK`

#### Get Patient Profile
```http
GET /patients/profile
```

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`

---

### Chatbot

#### Chat with AI
```http
POST /chatbot/chat
```

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "message": "I have a mole that's been changing color"
}
```

**Response:** `200 OK`
```json
{
  "response": "I can help analyze skin lesions. For the best assessment:\n1. Take a clear, well-lit photo...",
  "context": {
    "symptoms": ["mole"],
    "severity": "mild"
  }
}
```

---

### Reports

#### Generate PDF Report
```http
GET /reports/generate/{diagnosis_id}
```

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK` (PDF file download)

---

### Admin Dashboard

#### System Overview
```http
GET /admin/stats/overview
```

**Headers:** `Authorization: Bearer <token>` (Admin role required)

**Response:** `200 OK`
```json
{
  "total_diagnoses": 1250,
  "total_patients": 487,
  "total_users": 520,
  "model_accuracy": 0.86,
  "avg_confidence": 0.79,
  "high_risk_cases": 23
}
```

#### Condition Statistics
```http
GET /admin/stats/conditions
```

**Response:** `200 OK`
```json
{
  "condition_counts": {
    "MEL": 45,
    "BCC": 123,
    "NV": 680,
    "BKL": 220,
    "AK": 82,
    "SCC": 55,
    "DF": 30,
    "VASC": 15
  },
  "condition_percentages": {
    "MEL": 3.6,
    "BCC": 9.8,
    "NV": 54.4,
    ...
  }
}
```

#### Model Performance
```http
GET /admin/stats/model
```

**Response:** `200 OK`
```json
{
  "precision_per_class": {...},
  "recall_per_class": {...},
  "f1_per_class": {...},
  "confusion_matrix": [[...]],
  "overall_accuracy": 0.86
}
```

#### User Activity
```http
GET /admin/stats/activity
```

**Response:** `200 OK`
```json
{
  "active_users_today": 25,
  "active_users_week": 150,
  "active_users_month": 450,
  "new_registrations_week": 12,
  "avg_diagnoses_per_user": 2.5
}
```

#### System Health
```http
GET /admin/system/health
```

**Response:** `200 OK`
```json
{
  "api_status": "healthy",
  "database_status": "healthy",
  "model_status": "healthy",
  "avg_response_time_ms": 245.5,
  "error_rate": 0.02,
  "uptime_percentage": 99.8
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid input data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

Default rate limit: 60 requests per minute per user.

---

## Interactive Documentation

Visit these URLs when the backend is running:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
