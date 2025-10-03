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

// Enhanced API service interfaces
export interface ContentBlock {
  id: number
  raw_content: string
  type: 'json' | 'xml' | 'text'
  beautified_content: string
}

export interface BlocksResponse {
  file_id: string
  blocks: ContentBlock[]
}

export interface MultiAgentAnalysisResult {
  model: string
  focus: string
  [key: string]: any
}

export interface MultiAgentResponse {
  analysis_provider: string
  analysis: MultiAgentAnalysisResult[]
}

export interface UploadResponse {
  success: boolean
  message: string
  file_id?: string
}

// Enhanced API methods
export const api = {
  // Upload log file
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

  // Get parsed blocks from a file
  getFileBlocks: async (fileId: string): Promise<BlocksResponse> => {
    const response = await apiClient.get(`/file/${fileId}/blocks`)
    return response.data
  },

  // Analyze content with multi-agent system
  analyzeWithMultiAgent: async (content: string): Promise<MultiAgentResponse> => {
    const response = await apiClient.post('/analyze/multi-agent', { content })
    return response.data
  },

  // Health check with cache prevention
  healthCheck: async (): Promise<{ status: string; timestamp: string; version: string }> => {
    const response = await apiClient.get('/health')
    return response.data
  },

  // Direct axios methods for flexibility
  get: apiClient.get,
  post: apiClient.post,
  put: apiClient.put,
  delete: apiClient.delete
}

export default apiClient
