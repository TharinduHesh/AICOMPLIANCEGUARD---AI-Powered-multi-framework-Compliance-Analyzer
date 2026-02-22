import React from 'react'
import { useLocation, useParams } from 'react-router-dom'
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Chip,
  Alert,
  LinearProgress,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from '@mui/material'
import {
  CheckCircle as CheckIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  Info as InfoIcon,
  TrendingUp as TrendingIcon,
} from '@mui/icons-material'
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

function AnalysisResults() {
  const location = useLocation()
  const { analysisId } = useParams()
  const results = location.state?.results

  if (!results) {
    return (
      <Box>
        <Alert severity="error">
          No analysis results found. Please upload and analyze a document first.
        </Alert>
      </Box>
    )
  }

  const getRiskColor = (level) => {
    if (level === 'Low Risk') return 'success'
    if (level === 'Medium Risk') return 'warning'
    return 'error'
  }

  const getRiskIcon = (level) => {
    if (level === 'Low Risk') return <CheckIcon />
    if (level === 'Medium Risk') return <WarningIcon />
    return <ErrorIcon />
  }

  // Prepare CIA chart data
  const ciaData = results.cia_analysis
    ? [
        { name: 'Confidentiality', value: results.cia_analysis.cia_coverage.confidentiality },
        { name: 'Integrity', value: results.cia_analysis.cia_coverage.integrity },
        { name: 'Availability', value: results.cia_analysis.cia_coverage.availability },
      ]
    : []

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28']

  // Prepare compliance scores data
  const complianceData = Object.entries(results.compliance_results).map(([framework, data]) => ({
    name: framework.toUpperCase(),
    score: data.compliance_percentage || 0,
  }))

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Analysis Results
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Analysis ID: {analysisId} | Document: {results.file_name}
      </Typography>

      {/* Risk Prediction */}
      {results.risk_prediction && (
        <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
            <Typography variant="h5">Audit Risk Assessment</Typography>
            <Chip
              icon={getRiskIcon(results.risk_prediction.risk_level)}
              label={results.risk_prediction.risk_level}
              color={getRiskColor(results.risk_prediction.risk_level)}
              size="large"
            />
          </Box>
          <Typography variant="body2" color="text.secondary" paragraph>
            Confidence: {results.risk_prediction.confidence}%
          </Typography>
          
          <Grid container spacing={2} sx={{ mb: 2 }}>
            <Grid item xs={4}>
              <Typography variant="body2" color="text.secondary">Low Risk</Typography>
              <LinearProgress
                variant="determinate"
                value={results.risk_prediction.probability_distribution['Low Risk']}
                color="success"
                sx={{ height: 8, borderRadius: 1 }}
              />
              <Typography variant="caption">{results.risk_prediction.probability_distribution['Low Risk']}%</Typography>
            </Grid>
            <Grid item xs={4}>
              <Typography variant="body2" color="text.secondary">Medium Risk</Typography>
              <LinearProgress
                variant="determinate"
                value={results.risk_prediction.probability_distribution['Medium Risk']}
                color="warning"
                sx={{ height: 8, borderRadius: 1 }}
              />
              <Typography variant="caption">{results.risk_prediction.probability_distribution['Medium Risk']}%</Typography>
            </Grid>
            <Grid item xs={4}>
              <Typography variant="body2" color="text.secondary">High Risk</Typography>
              <LinearProgress
                variant="determinate"
                value={results.risk_prediction.probability_distribution['High Risk']}
                color="error"
                sx={{ height: 8, borderRadius: 1 }}
              />
              <Typography variant="caption">{results.risk_prediction.probability_distribution['High Risk']}%</Typography>
            </Grid>
          </Grid>

          {results.audit_readiness && (
            <Alert severity="info" sx={{ mb: 2 }}>
              <strong>Audit Readiness: {results.audit_readiness.readiness_level}</strong> (Score: {results.audit_readiness.audit_readiness_score}/100)
              <Typography variant="body2" sx={{ mt: 1 }}>
                {results.audit_readiness.recommendation}
              </Typography>
            </Alert>
          )}

          <Divider sx={{ my: 2 }} />
          
          <Typography variant="h6" gutterBottom>Recommendations</Typography>
          <List>
            {results.risk_prediction.recommendations.map((rec, idx) => (
              <ListItem key={idx}>
                <ListItemIcon>
                  <TrendingIcon color="primary" />
                </ListItemIcon>
                <ListItemText primary={rec} />
              </ListItem>
            ))}
          </List>
        </Paper>
      )}

      <Grid container spacing={3} sx={{ mb: 3 }}>
        {/* Compliance Scores */}
        <Grid item xs={12} md={6}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Framework Compliance Scores
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={complianceData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="score" fill="#8884d8" name="Compliance %" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* CIA Analysis */}
        {results.cia_analysis && (
          <Grid item xs={12} md={6}>
            <Card elevation={3}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  CIA Balance Analysis
                </Typography>
                <Box sx={{ textAlign: 'center', mb: 2 }}>
                  <Typography variant="h3" color="primary">
                    {results.cia_analysis.cia_balance_index}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Balance Index (0-100)
                  </Typography>
                  <Chip
                    label={results.cia_analysis.balance_rating}
                    color={results.cia_analysis.balance_rating === 'Excellent' ? 'success' : 'warning'}
                    sx={{ mt: 1 }}
                  />
                </Box>
                <ResponsiveContainer width="100%" height={200}>
                  <PieChart>
                    <Pie
                      data={ciaData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, value }) => `${name}: ${value.toFixed(1)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {ciaData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid>

      {/* Detailed Framework Results */}
      {Object.entries(results.compliance_results).map(([framework, data]) => (
        <Paper key={framework} elevation={2} sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            {framework.toUpperCase()} Analysis
          </Typography>
          <Grid container spacing={2} sx={{ mb: 2 }}>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="body2" color="text.secondary">Compliance %</Typography>
              <Typography variant="h4" color="primary">{data.compliance_percentage}%</Typography>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="body2" color="text.secondary">Matched Controls</Typography>
              <Typography variant="h4">{data.matched_controls_count}/{data.total_controls}</Typography>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="body2" color="text.secondary">Total Clauses</Typography>
              <Typography variant="h4">{data.total_clauses}</Typography>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography variant="body2" color="text.secondary">Matched Clauses</Typography>
              <Typography variant="h4">{data.matched_clauses}</Typography>
            </Grid>
          </Grid>

          {data.missing_controls && data.missing_controls.length > 0 && (
            <>
              <Divider sx={{ my: 2 }} />
              <Typography variant="subtitle1" gutterBottom>
                Missing Controls (Top 5)
              </Typography>
              <List dense>
                {data.missing_controls.slice(0, 5).map((control, idx) => (
                  <ListItem key={idx}>
                    <ListItemIcon>
                      <ErrorIcon color="error" />
                    </ListItemIcon>
                    <ListItemText
                      primary={`${control.control_id}: ${control.title}`}
                      secondary={`Category: ${control.category} | Priority: ${control.priority}`}
                    />
                  </ListItem>
                ))}
              </List>
            </>
          )}
        </Paper>
      ))}

      {/* CIA Recommendations */}
      {results.cia_analysis && results.cia_analysis.recommendations.length > 0 && (
        <Paper elevation={2} sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            CIA Balance Recommendations
          </Typography>
          <List>
            {results.cia_analysis.recommendations.map((rec, idx) => (
              <ListItem key={idx}>
                <ListItemIcon>
                  <InfoIcon color="info" />
                </ListItemIcon>
                <ListItemText primary={rec} />
              </ListItem>
            ))}
          </List>
        </Paper>
      )}
    </Box>
  )
}

export default AnalysisResults
