<template>
  <div class="transaction-flow-view fade-in">
    <!-- Header -->
    <div class="mb-8">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 mb-2">
            Transaction Flow Analysis
          </h1>
          <p class="text-gray-600">
            Step-by-step analysis of transaction {{ transactionId }}
          </p>
        </div>
        <div class="flex space-x-3">
          <button
            @click="analyzeWithManus"
            :disabled="isAnalyzing"
            class="btn-primary"
          >
            <svg v-if="isAnalyzing" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ isAnalyzing ? 'Analyzing...' : 'Analyze with Manus AI' }}
          </button>
          <RouterLink :to="`/transactions?file_id=${fileId}`" class="btn-secondary">
            Back to Transactions
          </RouterLink>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <div class="loading-spinner"></div>
      <span class="ml-3 text-gray-600">Loading transaction flow...</span>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="card bg-error-50 border-error-200">
      <div class="flex items-center space-x-3">
        <svg class="w-6 h-6 text-error-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div>
          <h3 class="text-lg font-semibold text-error-800">Error Loading Transaction Flow</h3>
          <p class="text-error-700">{{ error }}</p>
        </div>
      </div>
    </div>

    <!-- Transaction Flow Steps -->
    <div v-else-if="flowData" class="space-y-6">
      <!-- Manus AI Analysis Results -->
      <div v-if="manusAnalysis" class="card bg-primary-50 border-primary-200">
        <h3 class="text-lg font-semibold text-primary-800 mb-4">
          Manus AI Analysis Results
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h4 class="font-medium text-primary-700 mb-2">Summary</h4>
            <p class="text-sm text-primary-600">{{ manusAnalysis.summary }}</p>
          </div>
          <div>
            <h4 class="font-medium text-primary-700 mb-2">Risk Score</h4>
            <div class="flex items-center space-x-2">
              <div class="flex-1 bg-gray-200 rounded-full h-2">
                <div 
                  class="h-2 rounded-full transition-all duration-300"
                  :class="getRiskScoreColor(manusAnalysis.risk_score)"
                  :style="{ width: `${manusAnalysis.risk_score * 100}%` }"
                ></div>
              </div>
              <span class="text-sm font-medium text-primary-700">
                {{ Math.round(manusAnalysis.risk_score * 100) }}%
              </span>
            </div>
          </div>
        </div>
        <div v-if="manusAnalysis.key_findings?.length" class="mt-4">
          <h4 class="font-medium text-primary-700 mb-2">Key Findings</h4>
          <ul class="list-disc list-inside text-sm text-primary-600 space-y-1">
            <li v-for="finding in manusAnalysis.key_findings" :key="finding">{{ finding }}</li>
          </ul>
        </div>
        <div v-if="manusAnalysis.recommendations?.length" class="mt-4">
          <h4 class="font-medium text-primary-700 mb-2">Recommendations</h4>
          <ul class="list-disc list-inside text-sm text-primary-600 space-y-1">
            <li v-for="recommendation in manusAnalysis.recommendations" :key="recommendation">{{ recommendation }}</li>
          </ul>
        </div>
      </div>

      <!-- Flow Steps -->
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 mb-6">
          Transaction Flow Steps ({{ flowData.flow.length }} steps)
        </h3>
        
        <div class="space-y-4">
          <div
            v-for="(step, index) in flowData.flow"
            :key="index"
            class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow duration-200"
          >
            <!-- Step Header -->
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center space-x-3">
                <div class="flex-shrink-0 w-8 h-8 bg-primary-100 text-primary-600 rounded-full flex items-center justify-center text-sm font-medium">
                  {{ index + 1 }}
                </div>
                <div>
                  <h4 class="font-medium text-gray-900">Step {{ index + 1 }}</h4>
                  <p class="text-sm text-gray-500">{{ step.timestamp }}</p>
                </div>
              </div>
              
              <!-- Content Type Indicators -->
              <div class="flex space-x-2">
                <span v-if="step.has_json" class="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded">
                  JSON
                </span>
                <span v-if="step.has_xml" class="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded">
                  XML
                </span>
              </div>
            </div>

            <!-- Raw Content (always shown) -->
            <div class="mb-4">
              <h5 class="text-sm font-medium text-gray-700 mb-2">Raw Content</h5>
              <pre class="bg-gray-50 p-3 rounded text-sm text-gray-800 overflow-x-auto">{{ step.raw_content }}</pre>
            </div>

            <!-- Structured Content Display -->
            <ContentViewer
              :json-content="step.json_content"
              :xml-content="step.xml_content"
              :default-view="'json'"
            />
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
import ContentViewer from '@/components/ContentViewer.vue'

// Route and reactive data
const route = useRoute()
const transactionId = ref(route.params.id as string)
const fileId = ref(route.query.file_id as string)

const isLoading = ref(true)
const isAnalyzing = ref(false)
const error = ref<string | null>(null)
const flowData = ref<any>(null)
const manusAnalysis = ref<any>(null)

// Methods

const getRiskScoreColor = (score: number): string => {
  if (score < 0.3) return 'bg-green-500'
  if (score < 0.7) return 'bg-yellow-500'
  return 'bg-red-500'
}

const loadTransactionFlow = async () => {
  try {
    isLoading.value = true
    error.value = null
    
    const response = await api.get(`/transactions/${fileId.value}/${transactionId.value}/flow`)
    flowData.value = response.data
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to load transaction flow'
  } finally {
    isLoading.value = false
  }
}

const analyzeWithManus = async () => {
  try {
    isAnalyzing.value = true
    
    const response = await api.post(`/analyze/manus/${transactionId.value}?file_id=${fileId.value}`)
    manusAnalysis.value = response.data.analysis
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Manus AI analysis failed'
  } finally {
    isAnalyzing.value = false
  }
}

// Lifecycle
onMounted(() => {
  if (!fileId.value) {
    error.value = 'File ID is required'
    isLoading.value = false
    return
  }
  
  loadTransactionFlow()
})
</script>

<style scoped>
.transaction-flow-view {
  animation-duration: 0.6s;
}

pre {
  font-family: 'JetBrains Mono', 'Courier New', monospace;
  font-size: 0.875rem;
  line-height: 1.5;
}
</style>
