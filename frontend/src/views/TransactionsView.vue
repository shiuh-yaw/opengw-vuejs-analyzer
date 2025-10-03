<template>
  <div class="transactions-view fade-in">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">
        Transaction List
      </h1>
      <p class="text-gray-600">
        Browse and analyze individual transactions from uploaded log files
      </p>
    </div>

    <!-- File Selection -->
    <div v-if="!fileId" class="card mb-8">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Select a File</h3>
      <p class="text-gray-600 mb-4">
        Please upload a log file first or select from recently uploaded files.
      </p>
      <RouterLink to="/upload" class="btn-primary">
        Upload Log File
      </RouterLink>
    </div>

    <!-- Loading State -->
    <div v-else-if="isLoading" class="flex justify-center items-center py-12">
      <div class="loading-spinner"></div>
      <span class="ml-3 text-gray-600">Loading transactions...</span>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="card bg-error-50 border-error-200">
      <div class="flex items-center space-x-3">
        <svg class="w-6 h-6 text-error-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div>
          <h3 class="text-lg font-semibold text-error-800">Error Loading Transactions</h3>
          <p class="text-error-700">{{ error }}</p>
        </div>
      </div>
    </div>

    <!-- Transactions List -->
    <div v-else class="space-y-6">
      <!-- Summary Card -->
      <div class="card">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-lg font-semibold text-gray-900">
              File: {{ fileId }}
            </h3>
            <p class="text-sm text-gray-600 mt-1">
              {{ transactions.length }} unique transactions found
            </p>
          </div>
          <div class="flex space-x-3">
            <button
              @click="refreshTransactions"
              :disabled="isRefreshing"
              class="btn-secondary"
            >
              <svg v-if="isRefreshing" class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ isRefreshing ? 'Refreshing...' : 'Refresh' }}
            </button>
            <RouterLink to="/upload" class="btn-primary">
              Upload New File
            </RouterLink>
          </div>
        </div>
      </div>

      <!-- Search and Filter -->
      <div class="card">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
          <div class="flex-1 max-w-md">
            <label for="search" class="sr-only">Search transactions</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <input
                id="search"
                v-model="searchQuery"
                type="text"
                placeholder="Search transaction IDs..."
                class="input-field pl-10"
              />
            </div>
          </div>
          <div class="flex items-center space-x-3">
            <span class="text-sm text-gray-600">
              {{ filteredTransactions.length }} of {{ transactions.length }} transactions
            </span>
          </div>
        </div>
      </div>

      <!-- Transactions Grid -->
      <div v-if="filteredTransactions.length === 0" class="card text-center py-12">
        <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h3 class="text-lg font-medium text-gray-900 mb-2">No transactions found</h3>
        <p class="text-gray-600">
          {{ searchQuery ? 'Try adjusting your search criteria.' : 'No transactions available in this file.' }}
        </p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="transactionId in filteredTransactions"
          :key="transactionId"
          class="card hover:shadow-lg transition-shadow duration-200 cursor-pointer"
          @click="viewTransactionFlow(transactionId)"
        >
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-primary-100 text-primary-600 rounded-lg">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div>
                <h4 class="font-medium text-gray-900">Transaction</h4>
                <p class="text-sm text-gray-500">{{ transactionId }}</p>
              </div>
            </div>
          </div>

          <div class="space-y-3">
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-600">Status</span>
              <span class="status-pending">Ready for Analysis</span>
            </div>
            
            <div class="flex space-x-2">
              <button
                @click.stop="viewTransactionFlow(transactionId)"
                class="flex-1 btn-primary text-sm py-2"
              >
                View Flow
              </button>
              <button
                @click.stop="analyzeTransaction(transactionId)"
                :disabled="analyzingTransactions.has(transactionId)"
                class="flex-1 btn-secondary text-sm py-2"
              >
                <svg v-if="analyzingTransactions.has(transactionId)" class="animate-spin -ml-1 mr-1 h-3 w-3" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ analyzingTransactions.has(transactionId) ? 'Analyzing...' : 'Analyze' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { api } from '@/services/api'

// Route and router
const route = useRoute()
const router = useRouter()

// Reactive data
const fileId = ref(route.query.file_id as string)
const isLoading = ref(true)
const isRefreshing = ref(false)
const error = ref<string | null>(null)
const transactions = ref<string[]>([])
const searchQuery = ref('')
const analyzingTransactions = ref(new Set<string>())

// Computed
const filteredTransactions = computed(() => {
  if (!searchQuery.value) return transactions.value
  
  const query = searchQuery.value.toLowerCase()
  return transactions.value.filter(id => 
    id.toLowerCase().includes(query)
  )
})

// Methods
const loadTransactions = async () => {
  try {
    isLoading.value = true
    error.value = null
    
    const response = await api.get(`/transactions/${fileId.value}`)
    transactions.value = response.data
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to load transactions'
  } finally {
    isLoading.value = false
  }
}

const refreshTransactions = async () => {
  isRefreshing.value = true
  await loadTransactions()
  isRefreshing.value = false
}

const viewTransactionFlow = (transactionId: string) => {
  router.push({
    name: 'transaction-flow',
    params: { id: transactionId },
    query: { file_id: fileId.value }
  })
}

const analyzeTransaction = async (transactionId: string) => {
  try {
    analyzingTransactions.value.add(transactionId)
    
    await api.post(`/analyze/manus/${transactionId}?file_id=${fileId.value}`)
    
    // Navigate to flow view after analysis
    viewTransactionFlow(transactionId)
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Analysis failed'
  } finally {
    analyzingTransactions.value.delete(transactionId)
  }
}

// Lifecycle
onMounted(() => {
  if (fileId.value) {
    loadTransactions()
  } else {
    isLoading.value = false
  }
})
</script>

<style scoped>
.transactions-view {
  animation-duration: 0.6s;
}

.card:hover {
  transform: translateY(-2px);
}
</style>
