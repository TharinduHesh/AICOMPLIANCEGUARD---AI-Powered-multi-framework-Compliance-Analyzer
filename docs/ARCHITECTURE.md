# AIComplianceGuard - System Architecture

## Overview

AIComplianceGuard is a modular, secure, AI-powered compliance validation platform built on microservices architecture principles. The system processes compliance documents locally using transformer-based NLP models while ensuring data confidentiality through AES-256 encryption and zero-retention policies.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                         │
│  Dashboard | Upload | Analysis Results | Frameworks | About │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS/REST API
┌──────────────────────▼──────────────────────────────────────┐
│                   API Gateway (FastAPI)                      │
│     Authentication | Rate Limiting | Request Validation     │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
┌───────▼─────────┐          ┌────────▼────────┐
│  Core Modules   │          │  Security Layer │
│   (7 Modules)   │◄─────────┤   AES-256 Enc   │
└───────┬─────────┘          └─────────────────┘
        │
┌───────┴──────────────────────────────────────────┐
│  Module 1: Document Processor                    │
│  Module 2: NLP Compliance Intelligence           │
│  Module 3: CIA Validator                         │
│  Module 4: ISO 9001 Validator                    │
│  Module 5: Knowledge Graph Mapper                │
│  Module 6: Audit Risk Predictor                  │
│  Module 7: Security Layer                        │
└──────────────────────┬───────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
┌───────▼─────────┐          ┌────────▼────────┐
│ Framework Data  │          │ Firebase Store  │
│  ISO 27001/9001 │          │  (Metadata Only)│
│  NIST / GDPR    │          │                 │
└─────────────────┘          └─────────────────┘
```

---

## Core Modules

### Module 1: Document Processing Engine

**Purpose:** Extract and structure text from compliance documents

**Components:**
- PDF/DOCX parser (PyPDF2, python-docx)
- Text cleaner and normalizer
- Section segmentation algorithm
- Clause extraction engine
- Hash-based integrity validator (SHA-256)

**Flow:**
```
Upload → Validate → Extract Text → Clean → Segment → Extract Clauses → Hash
```

**Key Features:**
- Supports PDF and DOCX formats
- Maximum 10MB file size
- SHA-256 hash for integrity validation
- Automatic section detection
- Clause-level granularity

---

### Module 2: NLP Compliance Intelligence Engine

**Purpose:** Semantic understanding and classification of compliance clauses

**Components:**
- Sentence Transformer (all-MiniLM-L6-v2)
- Semantic similarity calculator (cosine similarity)
- Clause classifier
- Weak policy detector
- Missing control identifier

**Architecture:**
```
Input Clauses → Encode (Transformer) → Compute Similarity → 
Match Controls → Identify Gaps → Generate Recommendations
```

**Key Features:**
- 384-dimensional embeddings
- Semantic matching (threshold: 0.3)
- Multi-framework support
- Weak language detection (modal verbs)
- Top-3 control matching

**Performance:**
- Encoding: ~10ms per clause
- Similarity computation: O(n) for n controls
- Model size: ~80MB

---

### Module 3: CIA Validation Engine

**Purpose:** Analyze security control balance across CIA pillars

**Components:**
- CIA classifier (keyword-based + semantic)
- Balance Index calculator (Novel contribution)
- Imbalance detector
- Heatmap generator

**CIA Balance Index Formula:**
```
CBI = 100 - (σ(CIA%) / 47.14) × 100

where:
- σ(CIA%) = standard deviation of CIA coverage percentages
- 47.14 = theoretical maximum std dev for percentages
- Higher CBI = Better balance
```

**Classification Logic:**
- **Confidentiality:** access, authentication, encryption, privacy
- **Integrity:** accuracy, validation, audit trail, checksums
- **Availability:** uptime, backup, disaster recovery, failover

**Output:**
- Coverage percentages per pillar
- Balance Index (0-100)
- Balance Rating (Excellent/Good/Fair/Poor)
- Imbalance risks
- Heatmap data

**Thresholds:**
- Ideal coverage: 25-40% per pillar
- Excellent balance: CBI ≥ 85
- Poor balance: CBI < 50

---

### Module 4: ISO 9001 Validator

**Purpose:** Validate Quality Management System requirements

**Components:**
- QMS requirement checker
- PDCA cycle detector
- Maturity level assessor

**ISO 9001 Requirements:**
1. Documented Information (25%)
2. Risk-Based Thinking (25%)
3. Continuous Improvement (20%)
4. Customer Satisfaction (15%)
5. Leadership Commitment (15%)

**Scoring:**
```
Compliance Score = Σ(Requirement Score × Weight)
```

**Maturity Levels:**
- **Mature:** 4+ indicators present
- **Developing:** 3 indicators
- **Initial:** 1-2 indicators
- **Ad-hoc:** 0 indicators

---

### Module 5: Knowledge Graph Mapping Engine

**Purpose:** Cross-framework control mapping and unified compliance view

**Mappings:**
```
ISO 27001 ↔ ISO 9001
├─ A.5.1 → 7.5 (Documented Information)
├─ A.8.1 → 6.1 (Risk Assessment)
└─ A.18.1 → 9.3 (Management Review)

ISO 27001 ↔ NIST CSF
├─ A.5 → ID.GV, ID.RA (Governance & Risk)
├─ A.9 → PR.AC (Access Control)
└─ A.16 → RS.RP, RC.RP (Response & Recovery)

ISO 27001 ↔ GDPR
├─ A.9 → Art.32 (Security Measures)
├─ A.18 → Art.5, Art.24 (Lawfulness & Accountability)
└─ A.16 → Art.33, Art.34 (Breach Notification)
```

**Efficiency Calculation:**
```
Efficiency Gain = (Overlapping Controls / Total Controls) × 100
```

**Benefits:**
- Reduce duplicate compliance efforts
- Unified audit preparation
- Comprehensive compliance view

---

### Module 6: Audit Risk Predictor

**Purpose:** ML-based prediction of audit readiness and risk level

**Model:** Random Forest Classifier
- **Algorithm:** scikit-learn RandomForestClassifier
- **Estimators:** 100 trees
- **Max Depth:** 10
- **Features:** 4 (missing controls, CIA imbalance, weak statements, coverage%)

**Training Data:** 300 synthetic samples
- Low Risk: few missing, balanced CIA, high coverage (33%)
- Medium Risk: moderate gaps (33%)
- High Risk: many gaps, imbalanced (34%)

**Features:**
1. **Missing Controls Count** (0-50)
2. **CIA Imbalance Score** (0-100, inverse of balance index)
3. **Weak Statements Frequency** (per 100 clauses)
4. **Compliance Coverage %** (0-100)

**Output:**
- Risk Level (Low/Medium/High)
- Confidence percentage
- Probability distribution
- Feature contributions
- Recommendations

**Audit Readiness Score:**
```
Readiness = P(Low) × 1.0 + P(Medium) × 0.5 + P(High) × 0.0

Levels:
- Audit Ready: ≥ 80%
- Mostly Ready: 60-80%
- Preparing: 40-60%
- Not Ready: < 40%
```

---

### Module 7: Secure AI Processing Layer

**Purpose:** Ensure confidentiality, integrity, and availability of data

**Security Components:**

#### Confidentiality
- **AES-256 Encryption:** All uploaded files encrypted
- **No Raw Storage:** Documents processed in-memory
- **JWT Authentication:** Secure API access
- **RBAC:** Role-based access control

#### Integrity
- **SHA-256 Hashing:** File integrity validation
- **Tamper Detection:** Logging of all modifications
- **Digital Signatures:** (Future enhancement)

#### Availability
- **Docker Containers:** Isolated, resilient services
- **Auto-cleanup:** Temporary files deleted after 5 minutes
- **Health Checks:** Continuous monitoring

**Encryption Flow:**
```
Upload → Generate IV → AES-256 Encrypt → Store Encrypted → 
Process In-Memory → Delete Original → Retain Metadata Only
```

**Key Management:**
- 32-byte AES key from environment variable
- Unique IV per encryption
- Key rotation policy (recommended quarterly)

---

## Data Flow

### Document Analysis Flow

```
1. User uploads document (PDF/DOCX)
   └─> Security Layer: Encrypt & hash

2. Document Processor: Extract text & clauses
   └─> Integrity check via hash

3. NLP Engine: Classify clauses
   └─> Match against framework controls

4. CIA Validator: Analyze security balance
   └─> Calculate CIA Balance Index

5. ISO 9001 Validator (optional): QMS validation
   └─> PDCA cycle detection

6. Knowledge Graph: Cross-framework mapping
   └─> Identify overlaps

7. Audit Predictor: Risk prediction
   └─> ML model inference

8. Security Layer: Encrypt results
   └─> Store metadata only in Firebase

9. Response: Return analysis to user
   └─> Delete temporary files

10. Auto-Cleanup: After 5 minutes
    └─> Secure deletion (3-pass overwrite)
```

---

## Security Architecture

### CIA Triad Implementation

#### Confidentiality Measures
1. AES-256 encryption for all data
2. TLS 1.3 for data in transit
3. JWT token authentication
4. No cloud AI API calls (local processing)
5. Zero raw data retention

#### Integrity Measures
1. SHA-256 hash validation
2. Immutable audit logs
3. Digital signatures (planned)
4. Version control for frameworks

#### Availability Measures
1. Docker containerization
2. Health check endpoints
3. Graceful error handling
4. Automatic recovery mechanisms
5. Backup for framework data

### Threat Model

| Threat | Mitigation |
|--------|-----------|
| Data Exposure | AES-256 encryption, local processing |
| Man-in-the-Middle | TLS 1.3, certificate pinning |
| Unauthorized Access | JWT authentication, RBAC |
| Data Tampering | Hash validation, audit logging |
| Service Disruption | Docker, health checks, monitoring |
| Injection Attacks | Input validation, parameterized queries |

---

##Database Architecture

### Firebase Firestore Structure

```
/users/{userId}
  ├─ email
  ├─ created_at
  └─ role

/analyses/{analysisId}
  ├─ user_id
  ├─ file_hash
  ├─ frameworks_analyzed
  ├─ compliance_scores
  ├─ cia_metrics
  ├─ risk_level
  ├─ audit_readiness_score
  ├─ created_at
  └─ metadata (encrypted)

/logs/{logId}
  ├─ timestamp
  ├─ event_type
  ├─ user_id
  └─ details
```

**Data Retention Policy:**
- Analysis results: 90 days
- Audit logs: 1 year
- User data: Until account deletion
- Temporary files: 5 minutes (auto-delete)

---

## Scalability

### Horizontal Scaling
- Stateless API design
- Load balancer ready
- Containerized services
- Database sharding support

### Vertical Scaling
- GPU support for NLP models
- Batch processing capability
- Caching layer (Redis)

### Performance Metrics
- Document processing: ~2-5 seconds
- NLP analysis: ~3-7 seconds
- CIA analysis: ~1-2 seconds
- Risk prediction: <1 second
- **Total:** ~10-15 seconds per document

---

## Deployment Architecture

### Development
```
localhost:3000 (React Dev Server)
localhost:8000 (FastAPI with reload)
```

### Production
```
Load Balancer (nginx)
├─> Frontend Containers (3x)
└─> Backend Containers (5x)
    ├─> Module Workers
    └─> Database (Firebase)
```

### CI/CD Pipeline
```
Git Push → GitHub Actions → 
Build Docker Images → 
Run Tests → 
Deploy to Production → 
Health Check → 
Monitor
```

---

## Monitoring & Logging

### Health Checks
- `/health` - Overall system health
- `/api/v1/admin/system-health` - Detailed module status

### Metrics Tracked
- Request latency
- Error rates
- Model inference time
- Document processing time
- API endpoint usage

### Logging
- Structured JSON logs
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Centralized log aggregation (planned)

---

## Technology Stack Summary

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Material-UI, Recharts |
| Backend API | FastAPI, Python 3.11 |
| NLP/AI | Transformers, Sentence-BERT, spaCy |
| ML | Scikit-learn (Random Forest) |
| Document Processing | PyPDF2, python-docx |
| Security | Cryptography, PyJWT, AES-256 |
| Database | Firebase Firestore |
| Authentication | Firebase Auth, JWT |
| Deployment | Docker, Docker Compose |
| CI/CD | GitHub Actions |

---

## Future Enhancements

1. **Blockchain Audit Trail** - Immutable compliance history
2. **Explainable AI Module** - SHAP values for predictions
3. **LLM Integration** - GPT-4 for remediation drafting
4. **Mobile App** - iOS/Android native applications
5. **Real-time Collaboration** - Multi-user document editing
6. **Advanced Analytics** - Compliance trends over time
7. **API Rate Limiting** - Redis-based distributed rate limiter
8. **Multi-language Support** - NLP models for non-English documents

---

**Architecture designed for security, scalability, and maintainability**
