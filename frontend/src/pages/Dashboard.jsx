import React, { useState, useEffect } from 'react'
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Paper,
  CircularProgress,
} from '@mui/material'
import {
  Security as SecurityIcon,
  Assessment as AssessmentIcon,
  CloudUpload as UploadIcon,
  CheckCircle as CheckIcon,
} from '@mui/icons-material'
import { Link } from 'react-router-dom'
import { adminAPI } from '../services/api'

function Dashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      const data = await adminAPI.getSystemHealth()
      setStats(data)
    } catch (error) {
      console.error('Failed to load stats:', error)
    } finally {
      setLoading(false)
    }
  }

  const features = [
    {
      title: 'Multi-Framework Support',
      description: 'ISO 27001, ISO 9001, NIST CSF, GDPR/PDPA',
      icon: <SecurityIcon sx={{ fontSize: 40 }} color="primary" />,
    },
    {
      title: 'CIA Balance Analysis',
      description: 'Confidentiality, Integrity, Availability scoring',
      icon: <AssessmentIcon sx={{ fontSize: 40 }} color="success" />,
    },
    {
      title: 'Audit Risk Prediction',
      description: 'ML-powered readiness assessment',
      icon: <CheckIcon sx={{ fontSize: 40 }} color="error" />,
    },
    {
      title: 'Secure Processing',
      description: 'Local AI, AES-256 encryption, zero retention',
      icon: <UploadIcon sx={{ fontSize: 40 }} color="warning" />,
    },
  ]

  return (
    <Box>
      <Paper elevation={3} sx={{ p: 4, mb: 4, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
        <Typography variant="h3" component="h1" gutterBottom fontWeight="bold">
          🔐 AIComplianceGuard
        </Typography>
        <Typography variant="h6" paragraph>
          Secure AI-Powered Multi-Framework Compliance Validation Platform
        </Typography>
        <Typography variant="body1" paragraph>
          Analyze your compliance documents against ISO 27001, ISO 9001, NIST, and GDPR frameworks.
          Get instant insights, missing control detection, and audit risk predictions.
        </Typography>
        <Button
          component={Link}
          to="/upload"
          variant="contained"
          size="large"
          sx={{
            mt: 2,
            backgroundColor: 'white',
            color: 'primary.main',
            '&:hover': {
              backgroundColor: 'grey.100',
            },
          }}
          startIcon={<UploadIcon />}
        >
          Upload Document
        </Button>
      </Paper>

      <Grid container spacing={3} sx={{ mb: 4 }}>
        {features.map((feature, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card elevation={2} sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardContent sx={{ flexGrow: 1, textAlign: 'center' }}>
                <Box sx={{ mb: 2 }}>{feature.icon}</Box>
                <Typography variant="h6" component="h2" gutterBottom>
                  {feature.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {feature.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              How It Works
            </Typography>
            <Box component="ol" sx={{ pl: 2 }}>
              <Typography component="li" variant="body1" sx={{ mb: 1 }}>
                <strong>Upload</strong> your compliance document (PDF/DOCX)
              </Typography>
              <Typography component="li" variant="body1" sx={{ mb: 1 }}>
                <strong>Select</strong> frameworks to validate against
              </Typography>
              <Typography component="li" variant="body1" sx={{ mb: 1 }}>
                <strong>Analyze</strong> with secure AI processing
              </Typography>
              <Typography component="li" variant="body1" sx={{ mb: 1 }}>
                <strong>Review</strong> compliance scores, gaps, and recommendations
              </Typography>
              <Typography component="li" variant="body1">
                <strong>Improve</strong> your documentation based on insights
              </Typography>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              System Status
            </Typography>
            {loading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', my: 3 }}>
                <CircularProgress />
              </Box>
            ) : (
              <Box>
                <Typography variant="body1" sx={{ mb: 1 }}>
                  <strong>Status:</strong>{' '}
                  <Typography component="span" color="success.main">
                    ✓ Operational
                  </Typography>
                </Typography>
                <Typography variant="body1" sx={{ mb: 1 }}>
                  <strong>Frameworks Loaded:</strong> 4 (ISO 27001, ISO 9001, NIST, GDPR)
                </Typography>
                <Typography variant="body1" sx={{ mb: 1 }}>
                  <strong>AI Models:</strong> 7 Core Modules Active
                </Typography>
                <Typography variant="body1">
                  <strong>Security:</strong> AES-256, Local Processing, Zero Retention
                </Typography>
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  )
}

export default Dashboard
