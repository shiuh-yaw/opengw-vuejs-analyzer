<template>
  <div class="multi-agent-analysis">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <!-- Risk Analysis Agent -->
      <div v-if="riskAnalysis" class="agent-card risk-card">
        <div class="agent-header">
          <div class="flex items-center space-x-3">
            <div class="agent-icon bg-red-100 text-red-600">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-gray-900">Risk Analysis</h3>
              <p class="text-sm text-gray-600">{{ riskAnalysis.model }}</p>
            </div>
          </div>
        </div>
        
        <div class="agent-content">
          <div class="risk-score-section">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-medium text-gray-700">Risk Score</span>
              <span class="text-lg font-bold" :class="getRiskScoreColor(riskAnalysis.risk_score)">
                {{ Math.round(riskAnalysis.risk_score * 100) }}%
              </span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div 
                class="h-2 rounded-full transition-all duration-300"
                :class="getRiskScoreBarColor(riskAnalysis.risk_score)"
                :style="{ width: `${riskAnalysis.risk_score * 100}%` }"
              ></div>
            </div>
          </div>
          
          <div v-if="riskAnalysis.findings?.length" class="findings-section">
            <h4 class="text-sm font-medium text-gray-700 mb-2">Findings</h4>
            <ul class="space-y-1">
              <li v-for="finding in riskAnalysis.findings" :key="finding" class="text-sm text-gray-600 flex items-start space-x-2">
                <svg class="w-3 h-3 mt-0.5 text-red-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                </svg>
                <span>{{ finding }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Compliance Analysis Agent -->
      <div v-if="complianceAnalysis" class="agent-card compliance-card">
        <div class="agent-header">
          <div class="flex items-center space-x-3">
            <div class="agent-icon bg-blue-100 text-blue-600">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-gray-900">Compliance Analysis</h3>
              <p class="text-sm text-gray-600">{{ complianceAnalysis.model }}</p>
            </div>
          </div>
        </div>
        
        <div class="agent-content">
          <div class="compliance-status-section">
            <div class="flex items-center space-x-2 mb-3">
              <span class="text-sm font-medium text-gray-700">Status:</span>
              <span 
                class="px-2 py-1 text-xs font-medium rounded-full"
                :class="complianceAnalysis.compliance_status === 'ok' 
                  ? 'bg-green-100 text-green-800' 
                  : 'bg-red-100 text-red-800'"
              >
                {{ complianceAnalysis.compliance_status === 'ok' ? 'Compliant' : 'Issues Found' }}
              </span>
            </div>
          </div>
          
          <div v-if="complianceAnalysis.issues?.length" class="issues-section">
            <h4 class="text-sm font-medium text-gray-700 mb-2">Issues</h4>
            <ul class="space-y-1">
              <li v-for="issue in complianceAnalysis.issues" :key="issue" class="text-sm text-gray-600 flex items-start space-x-2">
                <svg class="w-3 h-3 mt-0.5 text-blue-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
                </svg>
                <span>{{ issue }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Fraud Analysis Agent -->
      <div v-if="fraudAnalysis" class="agent-card fraud-card">
        <div class="agent-header">
          <div class="flex items-center space-x-3">
            <div class="agent-icon bg-yellow-100 text-yellow-600">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-gray-900">Fraud Analysis</h3>
              <p class="text-sm text-gray-600">{{ fraudAnalysis.model }}</p>
            </div>
          </div>
        </div>
        
        <div class="agent-content">
          <div class="fraud-probability-section">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-medium text-gray-700">Fraud Probability</span>
              <span class="text-lg font-bold" :class="getFraudProbabilityColor(fraudAnalysis.fraud_probability)">
                {{ Math.round(fraudAnalysis.fraud_probability * 100) }}%
              </span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div 
                class="h-2 rounded-full transition-all duration-300"
                :class="getFraudProbabilityBarColor(fraudAnalysis.fraud_probability)"
                :style="{ width: `${fraudAnalysis.fraud_probability * 100}%` }"
              ></div>
            </div>
          </div>
          
          <div v-if="fraudAnalysis.indicators?.length" class="indicators-section">
            <h4 class="text-sm font-medium text-gray-700 mb-2">Indicators</h4>
            <ul class="space-y-1">
              <li v-for="indicator in fraudAnalysis.indicators" :key="indicator" class="text-sm text-gray-600 flex items-start space-x-2">
                <svg class="w-3 h-3 mt-0.5 text-yellow-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
                <span>{{ indicator }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- PSP Optimization Analysis Agent -->
      <div v-if="optimizationAnalysis" class="agent-card optimization-card">
        <div class="agent-header">
          <div class="flex items-center space-x-3">
            <div class="agent-icon bg-purple-100 text-purple-600">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-gray-900">PSP Optimization</h3>
              <p class="text-sm text-gray-600">{{ optimizationAnalysis.model }}</p>
            </div>
          </div>
        </div>
        
        <div class="agent-content">
          <div v-if="optimizationAnalysis.psp" class="psp-section">
            <div class="flex items-center space-x-2 mb-3">
              <span class="text-sm font-medium text-gray-700">PSP:</span>
              <span class="px-2 py-1 text-xs font-medium rounded-full bg-purple-100 text-purple-800">
                {{ optimizationAnalysis.psp }}
              </span>
            </div>
          </div>
          
          <div v-if="optimizationAnalysis.optimizations?.length" class="optimizations-section">
            <h4 class="text-sm font-medium text-gray-700 mb-2">Optimization Suggestions</h4>
            <ul class="space-y-1">
              <li v-for="optimization in optimizationAnalysis.optimizations" :key="optimization" class="text-sm text-gray-600 flex items-start space-x-2">
                <svg class="w-3 h-3 mt-0.5 text-purple-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                </svg>
                <span>{{ optimization }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Summary Section -->
    <div v-if="hasAnyAnalysis" class="mt-6 p-4 bg-gray-50 rounded-lg">
      <h3 class="text-lg font-semibold text-gray-900 mb-3">Analysis Summary</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
        <div v-if="riskAnalysis" class="summary-item">
          <span class="font-medium text-gray-700">Overall Risk:</span>
          <span :class="getRiskScoreColor(riskAnalysis.risk_score)" class="ml-2 font-semibold">
            {{ getRiskLevel(riskAnalysis.risk_score) }}
          </span>
        </div>
        <div v-if="complianceAnalysis" class="summary-item">
          <span class="font-medium text-gray-700">Compliance:</span>
          <span 
            class="ml-2 font-semibold"
            :class="complianceAnalysis.compliance_status === 'ok' ? 'text-green-600' : 'text-red-600'"
          >
            {{ complianceAnalysis.compliance_status === 'ok' ? 'Compliant' : 'Non-Compliant' }}
          </span>
        </div>
        <div v-if="fraudAnalysis" class="summary-item">
          <span class="font-medium text-gray-700">Fraud Risk:</span>
          <span :class="getFraudProbabilityColor(fraudAnalysis.fraud_probability)" class="ml-2 font-semibold">
            {{ getFraudLevel(fraudAnalysis.fraud_probability) }}
          </span>
        </div>
        <div v-if="optimizationAnalysis" class="summary-item">
          <span class="font-medium text-gray-700">PSP Optimizations:</span>
          <span class="ml-2 font-semibold text-purple-600">
            {{ optimizationAnalysis.optimizations?.length || 0 }} suggestions
          </span>
        </div>
      </div>

      <!-- PSP Optimization Analysis Agent -->
      <div v-if="optimizationAnalysis" class="agent-card optimization-card">
        <div class="agent-header">
          <div class="flex items-center space-x-3">
            <div class="agent-icon bg-purple-100 text-purple-600">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div>
              <h3 class="font-semibold text-gray-900">PSP Optimization</h3>
              <p class="text-sm text-gray-600">{{ optimizationAnalysis.model }}</p>
            </div>
          </div>
        </div>
        
        <div class="agent-content">
          <div v-if="optimizationAnalysis.psp" class="psp-section">
            <div class="flex items-center space-x-2 mb-3">
              <span class="text-sm font-medium text-gray-700">PSP:</span>
              <span class="px-2 py-1 text-xs font-medium rounded-full bg-purple-100 text-purple-800">
                {{ optimizationAnalysis.psp }}
              </span>
            </div>
          </div>
          
          <div v-if="optimizationAnalysis.optimizations?.length" class="optimizations-section">
            <h4 class="text-sm font-medium text-gray-700 mb-2">Optimization Suggestions</h4>
            <ul class="space-y-1">
              <li v-for="optimization in optimizationAnalysis.optimizations" :key="optimization" class="text-sm text-gray-600 flex items-start space-x-2">
                <svg class="w-3 h-3 mt-0.5 text-purple-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                </svg>
                <span>{{ optimization }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

// Props
interface Props {
  analysisResults?: Array<{
    model: string
    focus: string
    [key: string]: any
  }>
}

const props = defineProps<Props>()

// Computed properties to extract specific analysis results
const riskAnalysis = computed(() => 
  props.analysisResults?.find(result => result.focus === 'Risk')
)

const complianceAnalysis = computed(() => 
  props.analysisResults?.find(result => result.focus === 'Compliance')
)

const fraudAnalysis = computed(() => 
  props.analysisResults?.find(result => result.focus === 'Fraud')
)

const optimizationAnalysis = computed(() => 
  props.analysisResults?.find(result => result.focus === 'Optimization')
)

const hasAnyAnalysis = computed(() => 
  riskAnalysis.value || complianceAnalysis.value || fraudAnalysis.value || optimizationAnalysis.value
)

// Methods for styling
const getRiskScoreColor = (score: number): string => {
  if (score < 0.3) return 'text-green-600'
  if (score < 0.7) return 'text-yellow-600'
  return 'text-red-600'
}

const getRiskScoreBarColor = (score: number): string => {
  if (score < 0.3) return 'bg-green-500'
  if (score < 0.7) return 'bg-yellow-500'
  return 'bg-red-500'
}

const getFraudProbabilityColor = (probability: number): string => {
  if (probability < 0.3) return 'text-green-600'
  if (probability < 0.6) return 'text-yellow-600'
  return 'text-red-600'
}

const getFraudProbabilityBarColor = (probability: number): string => {
  if (probability < 0.3) return 'bg-green-500'
  if (probability < 0.6) return 'bg-yellow-500'
  return 'bg-red-500'
}

const getRiskLevel = (score: number): string => {
  if (score < 0.3) return 'Low'
  if (score < 0.7) return 'Medium'
  return 'High'
}

const getFraudLevel = (probability: number): string => {
  if (probability < 0.3) return 'Low'
  if (probability < 0.6) return 'Medium'
  return 'High'
}
</script>

<style scoped>
.agent-card {
  @apply bg-white border border-gray-200 rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow duration-200;
}

.agent-header {
  @apply mb-4 pb-3 border-b border-gray-100;
}

.agent-icon {
  @apply p-2 rounded-lg;
}

.agent-content {
  @apply space-y-4;
}

.risk-score-section,
.compliance-status-section,
.fraud-probability-section {
  @apply mb-4;
}

.findings-section,
.issues-section,
.indicators-section {
  @apply mt-3;
}

.summary-item {
  @apply flex items-center;
}
</style>
