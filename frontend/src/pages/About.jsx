import React from 'react'
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Chip,
  Divider,
} from '@mui/material'
import {
  Security as SecurityIcon,
  Speed as SpeedIcon,
  LocalHospital as HealthIcon,
  Psychology as AIIcon,
  Shield as ShieldIcon,
  Analytics as AnalyticsIcon,
} from '@mui/icons-material'

function About() {
  const modules = [
    {
      name: 'Document Processing Engine',
      description: 'PDF/DOCX extraction, text cleaning, section segmentation with integrity validation',
      icon: <SecurityIcon color="primary" />,
    },
    {
      name: 'NLP Compliance Intelligence',
      description: 'DistilBERT-based clause classification and semantic similarity matching',
      icon: <AIIcon color="secondary" />,
    },
    {
      name: 'CIA Validation Engine',
      description: 'Confidentiality, Integrity, Availability balance analysis with novel CIA Balance Index',
      icon: <ShieldIcon color="success" />,
    },
    {
      name: 'ISO 9001 Validator',
      description: 'Quality management system validation with PDCA cycle detection',
      icon: <HealthIcon color="warning" />,
    },
    {
      name: 'Knowledge Graph Mapper',
      description: 'Cross-framework control mapping (ISO 27001 ↔ ISO 9001 ↔ NIST ↔ GDPR)',
      icon: <AnalyticsIcon color="error" />,
    },
    {
      name: 'Audit Risk Predictor',
      description: 'ML-based audit risk prediction with Random Forest classification',
      icon: <SpeedIcon color="info" />,
    },
    {
      name: 'Secure AI Processing Layer',
      description: 'AES-256 encryption, local processing, zero data retention policy',
      icon: <SecurityIcon color="primary" />,
    },
  ]

  const features = [
    'Multi-framework support (ISO 27001, ISO 9001, NIST, GDPR)',
    'AI-powered clause classification using transformer models',
    'CIA Balance Index - Novel research contribution',
    'Audit risk prediction with ML',
    'Cross-framework knowledge graph mapping',
    'Secure local AI processing - no cloud API exposure',
    'AES-256 encryption for all data',
    'Zero data retention - automatic deletion',
    'Missing control detection and recommendations',
    'Weak policy statement identification',
  ]

  return (
    <Box>
      <Paper elevation={3} sx={{ p: 4, mb: 4, background: 'linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%)', color: 'white' }}>
        <Typography variant="h3" component="h1" gutterBottom fontWeight="bold">
          About AIComplianceGuard
        </Typography>
        <Typography variant="h6" paragraph>
          Secure AI-Powered Multi-Framework Compliance Validation Platform
        </Typography>
        <Typography variant="body1">
          Developed as an Individual Software Project (ISP) for cybersecurity research and commercial application.
          AIComplianceGuard addresses real-world compliance challenges faced by SMEs and organizations.
        </Typography>
      </Paper>

      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={6}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                🎯 Mission
              </Typography>
              <Typography variant="body1">
                To provide affordable, secure, and intelligent compliance validation tools that help organizations
                achieve and maintain compliance with multiple frameworks while protecting sensitive data.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                🔬 Research Contribution
              </Typography>
              <Typography variant="body1">
                Introduces the <strong>CIA-based Compliance Balance Index</strong>, a novel metric for measuring
                security control balance across Confidentiality, Integrity, and Availability pillars.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
        <Typography variant="h5" gutterBottom>
          ✨ Key Features
        </Typography>
        <Grid container spacing={2}>
          {features.map((feature, index) => (
            <Grid item xs={12} sm={6} key={index}>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Typography variant="body1">✓ {feature}</Typography>
              </Box>
            </Grid>
          ))}
        </Grid>
      </Paper>

      <Typography variant="h5" gutterBottom>
        🏗️ System Architecture - 7 Core Modules
      </Typography>
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {modules.map((module, index) => (
          <Grid item xs={12} md={6} key={index}>
            <Card elevation={2}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  {module.icon}
                  <Typography variant="h6" sx={{ ml: 1 }}>
                    Module {index + 1}
                  </Typography>
                </Box>
                <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                  {module.name}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {module.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
        <Typography variant="h5" gutterBottom>
          🔒 Security & Privacy
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <Typography variant="h6" color="primary" gutterBottom>
              Confidentiality
            </Typography>
            <ul>
              <li>
                <Typography variant="body2">No raw document storage</Typography>
              </li>
              <li>
                <Typography variant="body2">AES-256 encryption</Typography>
              </li>
              <li>
                <Typography variant="body2">Secure API endpoints with JWT</Typography>
              </li>
              <li>
                <Typography variant="body2">Role-based access control</Typography>
              </li>
            </ul>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="h6" color="success.main" gutterBottom>
              Integrity
            </Typography>
            <ul>
              <li>
                <Typography variant="body2">Hash validation of documents</Typography>
              </li>
              <li>
                <Typography variant="body2">Tamper-aware logging</Typography>
              </li>
              <li>
                <Typography variant="body2">Digital signature support</Typography>
              </li>
              <li>
                <Typography variant="body2">Audit trail</Typography>
              </li>
            </ul>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="h6" color="warning.main" gutterBottom>
              Availability
            </Typography>
            <ul>
              <li>
                <Typography variant="body2">Modular microservice architecture</Typography>
              </li>
              <li>
                <Typography variant="body2">Docker containerization</Typography>
              </li>
              <li>
                <Typography variant="body2">Metadata backup</Typography>
              </li>
              <li>
                <Typography variant="body2">Resilient design</Typography>
              </li>
            </ul>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  )
}

export default About
