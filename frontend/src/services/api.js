import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1'

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

// Auth API
export const authAPI = {
  register: async (companyId, companyName, password) => {
    const response = await api.post('/auth/register', {
      company_id: companyId,
      company_name: companyName,
      password,
    })
    return response.data
  },

  login: async (companyId, password) => {
    const response = await api.post('/auth/login', {
      company_id: companyId,
      password,
    })
    return response.data
  },

  getMe: async () => {
    const response = await api.get('/auth/me')
    return response.data
  },

  logout: () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  },
}

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

// Chat API
export const chatAPI = {
  newConversation: async () => {
    const response = await api.post('/chat/new')
    return response.data
  },

  sendMessage: async (conversationId, message) => {
    const response = await api.post('/chat/message', {
      conversation_id: conversationId,
      message,
    })
    return response.data
  },

  uploadDocument: async (conversationId, file) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('conversation_id', conversationId || '')
    const response = await api.post('/chat/upload-document', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  uploadAndAsk: async (conversationId, file, message, frameworks) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('message', message || 'Analyze this document for compliance')
    formData.append('conversation_id', conversationId || '')
    formData.append('frameworks', frameworks || 'iso27001')
    const response = await api.post('/chat/upload-and-ask', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  getConversation: async (conversationId) => {
    const response = await api.get(`/chat/conversation/${conversationId}`)
    return response.data
  },

  deleteConversation: async (conversationId) => {
    const response = await api.delete(`/chat/conversation/${conversationId}`)
    return response.data
  },

  getLLMStatus: async () => {
    const response = await api.get('/chat/llm/status')
    return response.data
  },
}
