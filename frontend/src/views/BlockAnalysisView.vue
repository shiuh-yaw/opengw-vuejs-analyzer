<template>
  <div class="block-analysis-view fade-in">
    <!-- Header -->
    <div class="mb-8">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 mb-2">
            Multi-Agent Block Analysis
          </h1>
          <p class="text-gray-600">
            Intelligent parsing and analysis of content blocks using multiple AI models
          </p>
        </div>
        <div class="flex space-x-3">
          <RouterLink to="/upload" class="btn-secondary">
            Upload New File
          </RouterLink>
        </div>
      </div>
    </div>

    <!-- File Selection -->
    <div v-if="!fileId" class="card mb-8">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Select a File</h3>
      <p class="text-gray-600 mb-4">
        Please upload a log file first to begin block analysis.
      </p>
      <RouterLink to="/upload" class="btn-primary">
        Upload Log File
      </RouterLink>
    </div>

    <!-- Loading State -->
    <div v-else-if="isLoading" class="flex justify-center items-center py-12">
      <div class="loading-spinner"></div>
      <span class="ml-3 text-gray-600">Parsing content blocks...</span>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="card bg-error-50 border-error-200">
      <div class="flex items-center space-x-3">
        <svg class="w-6 h-6 text-error-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div>
          <h3 class="text-lg font-semibold text-error-800">Error Loading Blocks</h3>
          <p class="text-error-700">{{ error }}</p>
        </div>
      </div>
    </div>

    <!-- Blocks Display -->
    <div v-else-if="blocksData" class="space-y-6">
      <!-- Summary Card -->
      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-lg font-semibold text-gray-900">
              File: {{ fileId }}
            </h3>
            <p class="text-sm text-gray-600 mt-1">
              {{ blocksData.blocks.length }} content blocks found
            </p>
          </div>
          <div class="flex space-x-3">
            <button
              @click="analyzeAllBlocks"
              :disabled="isAnalyzingAll"
              class="btn-primary"
            >
              <svg v-if="isAnalyzingAll" class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ isAnalyzingAll ? 'Analyzing All...' : 'Analyze All Blocks' }}
            </button>
            <button
              @click="refreshBlocks"
              :disabled="isRefreshing"
              class="btn-secondary"
            >
              <svg v-if="isRefreshing" class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ isRefreshing ? 'Refreshing...' : 'Refresh' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Blocks List -->
      <div v-if="blocksData.blocks.length === 0" class="card text-center py-12">
        <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h3 class="text-lg font-medium text-gray-900 mb-2">No content blocks found</h3>
        <p class="text-gray-600">
          The uploaded file does not contain any content enclosed in square brackets.
        </p>
      </div>

      <div v-else class="space-y-6">
        <div
          v-for="block in blocksData.blocks"
          :key="block.id"
          class="card hover:shadow-lg transition-shadow duration-200"
        >
          <!-- Block Header -->
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center space-x-3">
              <div class="flex-shrink-0 w-8 h-8 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center text-sm font-medium">
                {{ block.id }}
              </div>
              <div>
                <h4 class="font-medium text-gray-900">Block {{ block.id }}</h4>
                <div class="flex items-center space-x-2">
                  <span 
                    class="px-2 py-1 text-xs font-medium rounded"
                    :class="getTypeColor(block.type)"
                  >
                    {{ block.type.toUpperCase() }}
                  </span>
                </div>
              </div>
            </div>
            
            <div class="flex space-x-2">
              <button
                @click="analyzeBlock(block)"
                :disabled="analyzingBlocks.has(block.id)"
                class="btn-primary text-sm py-2 px-3"
              >
                <svg v-if="analyzingBlocks.has(block.id)" class="animate-spin -ml-1 mr-1 h-3 w-3" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ analyzingBlocks.has(block.id) ? 'Analyzing...' : 'Analyze' }}
              </button>
            </div>
          </div>

          <!-- Block Content -->
          <div class="space-y-4">
            <!-- Raw Content -->
            <div>
              <h5 class="text-sm font-medium text-gray-700 mb-2">Raw Content</h5>
              <pre class="bg-gray-50 p-3 rounded text-sm text-gray-800 overflow-x-auto max-h-32">{{ block.raw_content }}</pre>
            </div>

            <!-- Beautified Content -->
            <div v-if="block.type !== 'text'">
              <h5 class="text-sm font-medium text-gray-700 mb-2">
                Beautified {{ block.type.toUpperCase() }}
              </h5>
              <pre 
                class="p-3 rounded text-sm overflow-x-auto max-h-64"
                :class="getContentStyle(block.type)"
              >{{ block.beautified_content }}</pre>
            </div>

            <!-- Multi-Agent Analysis Results -->
            <div v-if="blockAnalysis[block.id]" class="mt-6">
              <h5 class="text-sm font-medium text-gray-700 mb-3">Multi-Agent Analysis Results</h5>
              <MultiAgentAnalysis :analysis-results="blockAnalysis[block.id]" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { api } from '@/services/api'
import MultiAgentAnalysis from '@/components/MultiAgentAnalysis.vue'

// Route and reactive data
const route = useRoute()
const fileId = ref(route.query.file_id as string)

const isLoading = ref(true)
const isRefreshing = ref(false)
const isAnalyzingAll = ref(false)
const error = ref<string | null>(null)
const blocksData = ref<any>(null)
const blockAnalysis = ref<Record<number, any>>({})
const analyzingBlocks = ref(new Set<number>())

// Methods
const loadBlocks = async () => {
  try {
    isLoading.value = true
    error.value = null
    
    const response = await api.get(`/file/${fileId.value}/blocks`)
    blocksData.value = response.data
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to load blocks'
  } finally {
    isLoading.value = false
  }
}

const refreshBlocks = async () => {
  isRefreshing.value = true
  await loadBlocks()
  isRefreshing.value = false
}

const analyzeBlock = async (block: any) => {
  try {
    analyzingBlocks.value.add(block.id)
    
    const response = await api.post('/analyze/multi-agent', {
      content: block.beautified_content || block.raw_content
    })
    
    blockAnalysis.value[block.id] = response.data.analysis
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Analysis failed'
  } finally {
    analyzingBlocks.value.delete(block.id)
  }
}

const analyzeAllBlocks = async () => {
  if (!blocksData.value?.blocks?.length) return
  
  isAnalyzingAll.value = true
  
  for (const block of blocksData.value.blocks) {
    await analyzeBlock(block)
  }
  
  isAnalyzingAll.value = false
}

const getTypeColor = (type: string): string => {
  switch (type) {
    case 'json':
      return 'bg-blue-100 text-blue-800'
    case 'xml':
      return 'bg-green-100 text-green-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

const getContentStyle = (type: string): string => {
  switch (type) {
    case 'json':
      return 'bg-blue-50 text-blue-900 border border-blue-200'
    case 'xml':
      return 'bg-green-50 text-green-900 border border-green-200'
    default:
      return 'bg-gray-50 text-gray-900 border border-gray-200'
  }
}

// Lifecycle
onMounted(() => {
  if (fileId.value) {
    loadBlocks()
  } else {
    isLoading.value = false
  }
})
</script>

<style scoped>
.block-analysis-view {
  animation-duration: 0.6s;
}

pre {
  font-family: 'JetBrains Mono', 'Courier New', monospace;
  font-size: 0.875rem;
  line-height: 1.5;
}
</style>
