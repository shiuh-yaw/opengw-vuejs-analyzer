<template>
  <div class="dashboard fade-in">
    <!-- Header Section -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">
        Transaction Analysis Dashboard
      </h1>
      <p class="text-gray-600">
        Monitor and analyze OpenGW payment transactions with AI-powered insights
      </p>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="card slide-up">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-primary-100 text-primary-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Total Transactions</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.totalTransactions }}</p>
          </div>
        </div>
      </div>

      <div class="card slide-up" style="animation-delay: 0.1s">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-success-100 text-success-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Successful</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.successfulTransactions }}</p>
          </div>
        </div>
      </div>

      <div class="card slide-up" style="animation-delay: 0.2s">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-error-100 text-error-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Failed</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.failedTransactions }}</p>
          </div>
        </div>
      </div>

      <div class="card slide-up" style="animation-delay: 0.3s">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-warning-100 text-warning-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Pending Analysis</p>
            <p class="text-2xl font-semibold text-gray-900">{{ stats.pendingAnalysis }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
        <div class="space-y-3">
          <RouterLink to="/upload" class="btn-primary w-full text-center block">
            Upload Transaction File
          </RouterLink>
          <RouterLink to="/transactions" class="btn-secondary w-full text-center block">
            View All Transactions
          </RouterLink>
          <RouterLink to="/analysis" class="btn-secondary w-full text-center block">
            Analysis History
          </RouterLink>
        </div>
      </div>

      <div class="card">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">System Status</h3>
        <div class="space-y-3">
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">Backend API</span>
            <span :class="systemStatus.api ? 'status-success' : 'status-error'">
              {{ systemStatus.api ? 'Online' : 'Offline' }}
            </span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">Cache Status</span>
            <span class="status-success">Disabled</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600">Last Updated</span>
            <span class="text-sm text-gray-500">{{ lastUpdated }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="card">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
      <div v-if="recentActivity.length === 0" class="text-center py-8 text-gray-500">
        No recent activity. Upload a transaction file to get started.
      </div>
      <div v-else class="space-y-3">
        <div
          v-for="activity in recentActivity"
          :key="activity.id"
          class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
        >
          <div class="flex items-center space-x-3">
            <div class="p-2 rounded-full bg-primary-100 text-primary-600">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <p class="text-sm font-medium text-gray-900">{{ activity.action }}</p>
              <p class="text-xs text-gray-500">{{ activity.timestamp }}</p>
            </div>
          </div>
          <span :class="getStatusClass(activity.status)">
            {{ activity.status }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { api } from '@/services/api'

// Reactive data
const stats = ref({
  totalTransactions: 0,
  successfulTransactions: 0,
  failedTransactions: 0,
  pendingAnalysis: 0
})

const systemStatus = ref({
  api: false
})

const lastUpdated = ref('')
const recentActivity = ref<Array<{
  id: string
  action: string
  timestamp: string
  status: string
}>>([])

// Methods
const getStatusClass = (status: string): string => {
  switch (status.toLowerCase()) {
    case 'completed':
    case 'success':
      return 'status-success'
    case 'failed':
    case 'error':
      return 'status-error'
    case 'pending':
    case 'processing':
      return 'status-warning'
    default:
      return 'status-pending'
  }
}

const checkSystemStatus = async () => {
  try {
    await api.healthCheck()
    systemStatus.value.api = true
  } catch (error) {
    systemStatus.value.api = false
    console.error('API health check failed:', error)
  }
}

const updateLastUpdated = () => {
  lastUpdated.value = new Date().toLocaleTimeString()
}

// Lifecycle
onMounted(async () => {
  await checkSystemStatus()
  updateLastUpdated()
  
  // Update timestamp every 30 seconds
  setInterval(updateLastUpdated, 30000)
})
</script>

<style scoped>
.dashboard {
  animation-duration: 0.6s;
}

.slide-up {
  animation-fill-mode: both;
}
</style>
