# AIComplianceGuard - API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Most endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

---

## Authentication Endpoints

### POST /auth/login

Login and receive JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

### GET /auth/me

Get current user information (requires authentication).

**Response:**
```json
{
  "email": "user@example.com",
  "user_type": "user"
}
```

---

## Compliance Endpoints

### POST /compliance/upload

Upload a compliance document for analysis.

**Content-Type:** `multipart/form-data`

**Request:**
- `file`: PDF or DOCX file (max 10MB)

**Response:**
```json
{
  "file_id": "unique_file_id",
  "file_name": "policy_document.pdf",
  "file_hash": "sha256_hash_string",
  "file_size": 524288,
  "uploaded_at": "2026-02-22T10:30:00Z"
}
```

### POST /compliance/analyze

Analyze uploaded document for compliance.

**Request Body:**
```json
{
  "file_id": "unique_file_id",
  "frameworks": ["iso27001", "iso9001", "nist", "gdpr"],
  "include_cia": true,
  "include_iso9001": true
}
```

**Response:**
```json
{
  "analysis_id": "unique_analysis_id",
  "file_name": "policy_document.pdf",
  "frameworks": ["iso27001", "iso9001"],
  "compliance_results": {
    "iso27001": {
      "framework": "iso27001",
      "total_clauses": 45,
      "matched_clauses": 38,
      "compliance_percentage": 65.8,
      "matched_controls_count": 75,
      "total_controls": 114,
      "missing_controls": [
        {
          "control_id": "A.8.1",
          "title": "User endpoint devices",
          "category": "Technical",
          "priority": "Critical"
        }
      ],
      "weak_clauses": [
        {
          "clause": "Access may be restricted...",
          "reason": "Weak language detected",
          "score": 0.45
        }
      ]
    }
  },
  "cia_analysis": {
    "total_clauses": 45,
    "cia_coverage": {
      "confidentiality": 35.5,
      "integrity": 42.2,
      "availability": 22.3
    },
    "cia_balance_index": 72.5,
    "balance_rating": "Good",
    "imbalances": [
      {
        "category": "availability",
        "type": "under_covered",
        "percentage": 22.3,
        "gap": 2.7,
        "severity": "Medium",
        "risk": "Availability controls are under-represented"
      }
    ],
    "recommendations": [
      "⚠️ Strengthen AVAILABILITY controls: Currently at 22.3%, should be 25-40%"
    ]
  },
  "risk_prediction": {
    "risk_level": "Medium Risk",
    "confidence": 78.5,
    "probability_distribution": {
      "Low Risk": 25.3,
      "Medium Risk": 58.2,
      "High Risk": 16.5
    },
    "recommendations": [
      "🟡 MEDIUM RISK: Improvements needed. Focus on key gaps."
    ]
  },
  "audit_readiness": {
    "audit_readiness_score": 67.8,
    "readiness_level": "Mostly Ready",
    "recommendation": "Address minor gaps and strengthen weak areas before audit."
  },
  "analyzed_at": "2026-02-22T10:35:00Z"
}
```

### GET /compliance/frameworks

Get list of supported compliance frameworks.

**Response:**
```json
{
  "frameworks": [
    {
      "id": "iso27001",
      "name": "ISO/IEC 27001:2022",
      "description": "Information Security Management System",
      "controls_count": 114
    },
    {
      "id": "iso9001",
      "name": "ISO 9001:2015",
      "description": "Quality Management System",
      "controls_count": 10
    }
  ]
}
```

---

## Analysis Endpoints

### POST /analysis/cia

Perform CIA analysis on document clauses.

**Request Body:**
```json
[
  {
    "text": "Access to systems must be controlled through authentication",
    "section": "Access Control"
  },
  {
    "text": "Data backups shall be performed daily",
    "section": "Business Continuity"
  }
]
```

**Response:**
```json
{
  "total_clauses": 2,
  "cia_coverage": {
    "confidentiality": 50.0,
    "integrity": 0.0,
    "availability": 50.0
  },
  "cia_balance_index": 85.7,
  "balance_rating": "Excellent",
  "imbalances": [],
  "recommendations": [
    "✅ CIA coverage is well-balanced across all three pillars."
  ]
}
```

### POST /analysis/risk-prediction

Predict audit risk based on analysis data.

**Request Body:**
```json
{
  "missing_controls_count": 15,
  "cia_balance_index": 72.5,
  "weak_clauses": [{"clause": "..."}],
  "total_clauses": 45,
  "compliance_percentage": 65.8
}
```

**Response:**
```json
{
  "risk_level": "Medium Risk",
  "confidence": 78.5,
  "probability_distribution": {
    "Low Risk": 25.3,
    "Medium Risk": 58.2,
    "High Risk": 16.5
  },
  "recommendations": [
    "🟡 MEDIUM RISK: Improvements needed.",
    "- Review and strengthen weak policy statements"
  ]
}
```

### GET /analysis/cia-definitions

Get CIA pillar definitions and indicators.

**Response:**
```json
{
  "confidentiality": {
    "name": "Confidentiality",
    "description": "Ensuring that information is accessible only to authorized individuals",
    "indicators": ["access", "authentication", "encryption", ...],
    "icon": "🔒"
  },
  "integrity": { ... },
  "availability": { ... }
}
```

---

## Admin Endpoints

*All admin endpoints require authentication*

### GET /admin/stats

Get system statistics.

**Response:**
```json
{
  "total_analyses": 152,
  "active_users": 23,
  "frameworks_supported": 4,
  "models_loaded": 7
}
```

### POST /admin/cleanup

Cleanup temporary files.

**Response:**
```json
{
  "message": "Cleaned up 5 temporary files",
  "count": 5
}
```

### GET /admin/system-health

Get detailed system health status.

**Response:**
```json
{
  "status": "healthy",
  "modules": {
    "document_processor": "operational",
    "nlp_engine": "operational",
    "cia_validator": "operational",
    "iso9001_validator": "operational",
    "knowledge_graph": "operational",
    "audit_predictor": "operational",
    "security_layer": "operational"
  },
  "disk_usage": "low",
  "memory_usage": "normal"
}
```

---

## Error Responses

All endpoints return standard error responses:

```json
{
  "error": "ValidationError",
  "message": "File size exceeds maximum (10MB)",
  "details": {
    "field": "file",
    "max_size": 10485760
  }
}
```

### HTTP Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Rate Limiting

API requests are rate-limited to 10 requests per minute per user.

**Rate Limit Headers:**
```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1708598400
```

---

## Security

### HTTPS

All production API calls must use HTTPS.

### Data Retention

- Uploaded documents are deleted automatically after 5 minutes
- Only encrypted metadata is stored
- No raw document content is retained

### Encryption

- All data encrypted with AES-256
- JWT tokens expire after 24 hours
- Secure file upload with hash validation

---

## Examples

### Python

```python
import requests

# Login
response = requests.post('http://localhost:8000/api/v1/auth/login', json={
    'email': 'user@example.com',
    'password': 'password'
})
token = response.json()['access_token']

# Upload document
files = {'file': open('policy.pdf', 'rb')}
headers = {'Authorization': f'Bearer {token}'}
response = requests.post('http://localhost:8000/api/v1/compliance/upload', 
                        files=files, headers=headers)
file_id = response.json()['file_id']

# Analyze document
response = requests.post('http://localhost:8000/api/v1/compliance/analyze',
                        json={
                            'file_id': file_id,
                            'frameworks': ['iso27001'],
                            'include_cia': True
                        },
                        headers=headers)
results = response.json()
print(f"Compliance: {results['compliance_results']['iso27001']['compliance_percentage']}%")
```

### JavaScript (Axios)

```javascript
const axios = require('axios');

const API_URL = 'http://localhost:8000/api/v1';

// Login
const login = async () => {
  const response = await axios.post(`${API_URL}/auth/login`, {
    email: 'user@example.com',
    password: 'password'
  });
  return response.data.access_token;
};

// Upload and analyze
const analyzeDocument = async (token, file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const uploadResponse = await axios.post(`${API_URL}/compliance/upload`, formData, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'multipart/form-data'
    }
  });
  
  const fileId = uploadResponse.data.file_id;
  
  const analysisResponse = await axios.post(`${API_URL}/compliance/analyze`, {
    file_id: fileId,
    frameworks: ['iso27001'],
    include_cia: true
  }, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  return analysisResponse.data;
};
```

---

## Interactive Documentation

Visit `http://localhost:8000/api/v1/docs` for interactive Swagger UI documentation with live testing capabilities.
