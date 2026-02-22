import React, { useState, useEffect } from 'react'
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Chip,
  CircularProgress,
  Alert,
} from '@mui/material'
import {
  Security as SecurityIcon,
  Assessment as AssessmentIcon,
  Policy as PolicyIcon,
  VerifiedUser as VerifiedIcon,
} from '@mui/icons-material'
import { complianceAPI } from '../services/api'

function Frameworks() {
  const [frameworks, setFrameworks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadFrameworks()
  }, [])

  const loadFrameworks = async () => {
    try {
      const data = await complianceAPI.getFrameworks()
      setFrameworks(data.frameworks)
    } catch (error) {
      setError('Failed to load frameworks')
      console.error('Error loading frameworks:', error)
    } finally {
      setLoading(false)
    }
  }

  const getFrameworkIcon = (id) => {
    switch (id) {
      case 'iso27001':
        return <SecurityIcon sx={{ fontSize: 40 }} color="primary" />
      case 'iso9001':
        return <VerifiedIcon sx={{ fontSize: 40 }} color="success" />
      case 'nist':
        return <PolicyIcon sx={{ fontSize: 40 }} color="error" />
      case 'gdpr':
        return <AssessmentIcon sx={{ fontSize: 40 }} color="warning" />
      default:
        return <SecurityIcon sx={{ fontSize: 40 }} />
    }
  }

  const getFrameworkColor = (id) => {
    switch (id) {
      case 'iso27001':
        return 'primary'
      case 'iso9001':
        return 'success'
      case 'nist':
        return 'error'
      case 'gdpr':
        return 'warning'
      default:
        return 'default'
    }
  }

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
        <CircularProgress />
      </Box>
    )
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>
  }

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Supported Compliance Frameworks
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        AIComplianceGuard supports multiple compliance frameworks for comprehensive validation
      </Typography>

      <Grid container spacing={3}>
        {frameworks.map((framework) => (
          <Grid item xs={12} md={6} key={framework.id}>
            <Card elevation={3} sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  {getFrameworkIcon(framework.id)}
                  <Box sx={{ ml: 2, flexGrow: 1 }}>
                    <Typography variant="h5" component="h2">
                      {framework.name}
                    </Typography>
                    <Chip
                      label={`${framework.controls_count} Controls`}
                      size="small"
                      color={getFrameworkColor(framework.id)}
                      sx={{ mt: 1 }}
                    />
                  </Box>
                </Box>

                <Typography variant="body2" color="text.secondary" paragraph>
                  {framework.description}
                </Typography>

                <Box sx={{ mt: 2, p: 2, backgroundColor: 'background.default', borderRadius: 1 }}>
                  <Typography variant="body2" fontWeight="bold" gutterBottom>
                    Key Features:
                  </Typography>
                  <ul style={{ margin: 0, paddingLeft: 20 }}>
                    <li>
                      <Typography variant="body2">Automated control mapping</Typography>
                    </li>
                    <li>
                      <Typography variant="body2">Missing control detection</Typography>
                    </li>
                    <li>
                      <Typography variant="body2">Compliance scoring</Typography>
                    </li>
                    <li>
                      <Typography variant="body2">Gap analysis & recommendations</Typography>
                    </li>
                  </ul>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Card elevation={3} sx={{ mt: 4, p: 3, backgroundColor: 'info.lighter' }}>
        <Typography variant="h6" gutterBottom>
          Cross-Framework Mapping
        </Typography>
        <Typography variant="body2" paragraph>
          Our Knowledge Graph Engine maps controls across different frameworks, helping you:
        </Typography>
        <ul>
          <li>
            <Typography variant="body2">Identify overlapping controls between frameworks</Typography>
          </li>
          <li>
            <Typography variant="body2">Reduce duplicate compliance efforts</Typography>
          </li>
          <li>
            <Typography variant="body2">Achieve unified compliance view</Typography>
          </li>
          <li>
            <Typography variant="body2">Demonstrate comprehensive compliance during audits</Typography>
          </li>
        </ul>
      </Card>
    </Box>
  )
}

export default Frameworks
