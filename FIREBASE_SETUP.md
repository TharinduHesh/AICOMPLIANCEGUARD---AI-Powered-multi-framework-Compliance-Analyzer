# Firebase Setup Guide for AIComplianceGuard

## Overview
Firebase Firestore stores **ONLY metadata** from compliance analyses:
- Compliance scores
- Risk predictions
- CIA metrics
- Audit logs

**🔒 SECURITY NOTE:** Raw documents are NEVER stored in Firebase. All processing is local.

---

## Setup Instructions

### 1. Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project"
3. Enter project name: `aicomplianceguard` (or your choice)
4. Disable Google Analytics (optional)
5. Click "Create project"

### 2. Enable Firestore Database

1. In Firebase Console, go to **Firestore Database**
2. Click "Create database"
3. Select **Production mode** (recommended) or Test mode
4. Choose your database location (e.g., `us-central`)
5. Click "Enable"

### 3. Generate Service Account Credentials

1. Go to **Project Settings** (gear icon) → **Service accounts**
2. Click "Generate new private key"
3. Download the JSON file
4. Rename it to `firebase-credentials.json`
5. Place it in the project root directory:
   ```
   ISP Project/
   ├── backend/
   ├── frontend/
   ├── firebase-credentials.json  ← Place here
   └── ...
   ```

### 4. Configure Environment Variables

Edit your `.env` file:

```env
# Firebase Configuration
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
```

Replace `your-project-id` with your actual Firebase project ID (found in Project Settings).

### 5. Set Firestore Security Rules

In Firebase Console → Firestore Database → Rules, set:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Compliance analyses - authenticated access only
    match /compliance_analyses/{analysisId} {
      allow read: if request.auth != null;
      allow write: if request.auth != null;
    }
    
    // Audit logs - admin only
    match /audit_logs/{logId} {
      allow read: if request.auth != null && request.auth.token.admin == true;
      allow write: if request.auth != null;
    }
  }
}
```

### 6. Verify Installation

Start the backend and check logs for:
```
✅ Firebase initialized successfully
```

Or test via API:
```bash
curl http://localhost:8000/api/v1/admin/firebase-stats
```

---

## Firestore Collections Structure

### `compliance_analyses`
```json
{
  "analysis_id": "string",
  "file_name": "string",
  "file_hash": "string (SHA-256)",
  "frameworks": ["iso27001", "nist"],
  "compliance_scores": {
    "iso27001": {
      "compliance_percentage": 78.5,
      "matched_controls_count": 89,
      "total_controls": 114
    }
  },
  "risk_prediction": {
    "risk_level": "Medium Risk",
    "confidence": 87
  },
  "cia_metrics": {
    "balance_index": 72.4,
    "confidentiality": 85,
    "integrity": 70,
    "availability": 62
  },
  "analyzed_at": "2026-02-24T10:30:00Z",
  "stored_at": "Firebase Timestamp",
  "retention_until": "2026-05-25T00:00:00Z"
}
```

### `audit_logs`
```json
{
  "event_type": "document_upload",
  "file_name": "compliance_policy.pdf",
  "file_size": 1048576,
  "file_hash": "sha256_hash_here",
  "ip_address": "192.168.1.100",
  "timestamp": "Firebase Timestamp"
}
```

---

## Data Retention

- **Metadata retention**: 90 days (automatic cleanup)
- **Audit logs retention**: 1 year
- **Raw documents**: NEVER stored (deleted immediately after processing)

Run cleanup manually:
```bash
curl -X POST http://localhost:8000/api/v1/admin/firebase-cleanup
```

---

## Running Without Firebase

The system works perfectly without Firebase:
- All features remain functional
- Data stored in browser localStorage
- Logs: "Firebase disabled - metadata not stored"

To disable Firebase, simply don't provide credentials or set:
```env
FIREBASE_CREDENTIALS_PATH=
```

---

## Security Best Practices

1. ✅ **Never commit** `firebase-credentials.json` to git
2. ✅ Keep credentials file permissions restricted (chmod 600)
3. ✅ Use environment-specific Firebase projects (dev/prod)
4. ✅ Enable Firestore security rules
5. ✅ Monitor Firebase usage quotas
6. ✅ Regularly audit Firebase access logs

---

## Troubleshooting

### "Firebase credentials not found"
- Ensure `firebase-credentials.json` exists in the correct location
- Check FIREBASE_CREDENTIALS_PATH in `.env`

### "Permission denied"
- Verify Firestore security rules
- Check service account has "Cloud Datastore User" role

### "Firebase already initialized"
- This is normal if restarting the app - just a warning

### High Firebase costs
- Review retention policies
- Run cleanup command regularly
- Monitor Firestore usage in Firebase Console

---

## Cost Estimation

Firebase Spark Plan (Free tier):
- ✅ 1 GB storage
- ✅ 50,000 reads/day
- ✅ 20,000 writes/day

For typical usage (10-50 analyses/day):
- **Expected cost**: $0/month (within free tier)

---

## Support

- Firebase Documentation: https://firebase.google.com/docs/firestore
- Project Issues: [GitHub Issues](https://github.com/your-repo/issues)
