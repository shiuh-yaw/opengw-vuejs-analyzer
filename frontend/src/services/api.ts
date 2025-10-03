import axios, { type AxiosInstance, type AxiosRequestConfig, type AxiosResponse } from 'axios'

// Cache prevention utility
const getCacheBuster = (): string => {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
}

// Create axios instance with cache prevention
const apiClient: AxiosInstance = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Expires': '0'
  }
})

// Request interceptor to add cache busting
apiClient.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    // Add cache buster to all requests
    const cacheBuster = getCacheBuster()
    
    if (config.params) {
      config.params._cb = cacheBuster
    } else {
      config.params = { _cb: cacheBuster }
    }
    
    // Add timestamp header
    config.headers = {
      ...config.headers,
      'X-Request-Time': Date.now().toString(),
      'X-Cache-Buster': cacheBuster
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    // Add cache prevention headers to response handling
    response.headers['cache-control'] = 'no-cache, no-store, must-revalidate'
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      console.error('Unauthorized access')
    } else if (error.response?.status >= 500) {
      // Handle server errors
      console.error('Server error:', error.response.data)
    }
    return Promise.reject(error)
  }
)

// API service interface
export interface TransactionData {
  id: string
  timestamp: string
  amount: number
  currency: string
  status: 'success' | 'failed' | 'pending' | 'cancelled'
  gateway: string
  merchant_id: string
  transaction_type: string
  [key: string]: any
}

export interface AnalysisResult {
  transaction_id: string
  analysis: {
    status: string
    issues: string[]
    recommendations: string[]
    risk_score: number
    patterns: string[]
  }
  manus_insights?: {
    summary: string
    key_findings: string[]
    recommendations: string[]
    confidence_score: number
  }
}

export interface UploadResponse {
  success: boolean
  message: string
  file_id?: string
  transactions_count?: number
}

// API methods
export const api = {
  // Upload transaction file
  uploadFile: async (file: File): Promise<UploadResponse> => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('_cb', getCacheBuster())
    
    const response = await apiClient.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  },

  // Get transactions list
  getTransactions: async (fileId?: string): Promise<TransactionData[]> => {
    const params = fileId ? { file_id: fileId } : {}
    const response = await apiClient.get('/transactions', { params })
    return response.data
  },

  // Analyze single transaction
  analyzeTransaction: async (transactionId: string): Promise<AnalysisResult> => {
    const response = await apiClient.post(`/analyze/${transactionId}`)
    return response.data
  },

  // Analyze transaction with Manus AI
  analyzeWithManus: async (transactionId: string): Promise<AnalysisResult> => {
    const response = await apiClient.post(`/analyze/manus/${transactionId}`)
    return response.data
  },

  // Batch analyze transactions
  batchAnalyze: async (transactionIds: string[]): Promise<AnalysisResult[]> => {
    const response = await apiClient.post('/analyze/batch', {
      transaction_ids: transactionIds
    })
    return response.data
  },

  // Get analysis history
  getAnalysisHistory: async (): Promise<AnalysisResult[]> => {
    const response = await apiClient.get('/analysis/history')
    return response.data
  },

  // Health check with cache prevention
  healthCheck: async (): Promise<{ status: string; timestamp: string; version: string }> => {
    const response = await apiClient.get('/health')
    return response.data
  }
}

export default apiClient
