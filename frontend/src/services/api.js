import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add request interceptor for authentication
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Compliance API
export const complianceAPI = {
  uploadDocument: async (file) => {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await api.post('/compliance/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  analyzeDocument: async (fileId, frameworks = ['iso27001'], includeCIA = true, includeISO9001 = false) => {
    const response = await api.post('/compliance/analyze', {
      file_id: fileId,
      frameworks,
      include_cia: includeCIA,
      include_iso9001: includeISO9001,
    })
    return response.data
  },

  getFrameworks: async () => {
    const response = await api.get('/compliance/frameworks')
    return response.data
  },
}

// Analysis API
export const analysisAPI = {
  analyzeCIA: async (clauses) => {
    const response = await api.post('/analysis/cia', { clauses })
    return response.data
  },

  predictRisk: async (analysisData) => {
    const response = await api.post('/analysis/risk-prediction', analysisData)
    return response.data
  },

  getCIADefinitions: async () => {
    const response = await api.get('/analysis/cia-definitions')
    return response.data
  },
}

// Auth API
export const authAPI = {
  login: async (email, password) => {
    const response = await api.post('/auth/login', { email, password })
    return response.data
  },

  logout: async () => {
    const response = await api.post('/auth/logout')
    return response.data
  },

  getCurrentUser: async () => {
    const response = await api.get('/auth/me')
    return response.data
  },
}

// Admin API
export const adminAPI = {
  getStats: async () => {
    const response = await api.get('/admin/stats')
    return response.data
  },

  cleanupFiles: async () => {
    const response = await api.post('/admin/cleanup')
    return response.data
  },

  getSystemHealth: async () => {
    const response = await api.get('/admin/system-health')
    return response.data
  },
}

export default api
