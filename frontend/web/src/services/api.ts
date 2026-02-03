import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add token to requests
apiClient.interceptors.request.use((config: any) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

// Handle response errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth endpoints
export const authAPI = {
  register: (username: string, email: string, password: string) =>
    apiClient.post('/users/register/', { username, email, password }),
  login: (username: string, password: string) =>
    apiClient.post('/users/login/', { username, password })
}

// Dataset endpoints
export const datasetAPI = {
  list: (page = 1) => apiClient.get(`/datasets/?page=${page}`),
  get: (id: any) => apiClient.get(`/datasets/${id}/`),
  uploadCSV: (file: any) => {
    const formData = new FormData()
    formData.append('file', file)
    return apiClient.post('/datasets/upload_csv/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },
  getEquipment: (id: any) => apiClient.get(`/datasets/${id}/equipment/`),
  generatePDF: (id: any) => apiClient.get(`/datasets/${id}/generate_pdf/`, { responseType: 'blob' })
}

// Equipment endpoints
export const equipmentAPI = {
  list: (page = 1) => apiClient.get(`/equipment/?page=${page}`),
  get: (id: any) => apiClient.get(`/equipment/${id}/`)
}

// Analytics endpoints
export const analyticsAPI = {
  getSummary: () => apiClient.get('/summary/summary/')
}

export default apiClient
