<template>
  <div class="upload-view fade-in">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">
        Upload Transaction File
      </h1>
      <p class="text-gray-600">
        Upload your OpenGW transaction log files for AI-powered analysis
      </p>
    </div>

    <!-- Upload Area -->
    <div class="card mb-8">
      <div
        @drop="handleDrop"
        @dragover.prevent
        @dragenter.prevent
        @dragleave="handleDragLeave"
        :class="['upload-area', { 'dragover': isDragOver }]"
        @click="triggerFileInput"
      >
        <input
          ref="fileInput"
          type="file"
          accept=".json"
          @change="handleFileSelect"
          class="hidden"
        />
        
        <div class="text-center">
          <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" stroke="currentColor" fill="none" viewBox="0 0 48 48">
            <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
          
          <div v-if="!isUploading">
            <p class="text-lg font-medium text-gray-900 mb-2">
              Drop your JSON file here, or click to browse
            </p>
            <p class="text-sm text-gray-500">
              Supports OpenGW transaction log files in JSON format
            </p>
          </div>
          
          <div v-else class="flex flex-col items-center">
            <div class="loading-spinner mb-4"></div>
            <p class="text-lg font-medium text-gray-900">
              Uploading and processing file...
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Upload Status -->
    <div v-if="uploadStatus" class="card mb-8">
      <div class="flex items-start space-x-3">
        <div v-if="uploadStatus.success" class="p-2 rounded-full bg-success-100 text-success-600">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <div v-else class="p-2 rounded-full bg-error-100 text-error-600">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </div>
        
        <div class="flex-1">
          <h3 class="text-lg font-semibold" :class="uploadStatus.success ? 'text-success-800' : 'text-error-800'">
            {{ uploadStatus.success ? 'Upload Successful' : 'Upload Failed' }}
          </h3>
          <p class="text-sm text-gray-600 mt-1">
            {{ uploadStatus.message }}
          </p>
          
          <div v-if="uploadStatus.success" class="mt-4">
            <div class="flex space-x-3">
              <button
                @click="resetUpload"
                class="btn-secondary"
              >
                Upload Another File
              </button>
              <RouterLink
                :to="`/blocks?file_id=${uploadStatus.file_id}`"
                class="btn-primary"
              >
                Analyze Blocks
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- File Requirements -->
    <div class="card">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">File Requirements</h3>
      <div class="space-y-3 text-sm text-gray-600">
        <div class="flex items-start space-x-2">
          <svg class="w-4 h-4 text-primary-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <span>JSON format only (.json extension)</span>
        </div>
        <div class="flex items-start space-x-2">
          <svg class="w-4 h-4 text-primary-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <span>Maximum file size: 50MB</span>
        </div>
        <div class="flex items-start space-x-2">
          <svg class="w-4 h-4 text-primary-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <span>OpenGW transaction log format</span>
        </div>
        <div class="flex items-start space-x-2">
          <svg class="w-4 h-4 text-primary-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <span>Must contain transaction data with required fields</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { api, type UploadResponse } from '@/services/api'

// Reactive data
const fileInput = ref<HTMLInputElement>()
const isDragOver = ref(false)
const isUploading = ref(false)
const uploadStatus = ref<UploadResponse | null>(null)

// Methods
const triggerFileInput = () => {
  if (!isUploading.value) {
    fileInput.value?.click()
  }
}

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    uploadFile(file)
  }
}

const handleDrop = (event: DragEvent) => {
  event.preventDefault()
  isDragOver.value = false
  
  const file = event.dataTransfer?.files[0]
  if (file) {
    uploadFile(file)
  }
}

const handleDragLeave = (event: DragEvent) => {
  // Only set isDragOver to false if we're leaving the drop zone entirely
  const rect = (event.currentTarget as HTMLElement).getBoundingClientRect()
  const x = event.clientX
  const y = event.clientY
  
  if (x < rect.left || x > rect.right || y < rect.top || y > rect.bottom) {
    isDragOver.value = false
  }
}

const uploadFile = async (file: File) => {
  if (!file.name.endsWith('.json')) {
    uploadStatus.value = {
      success: false,
      message: 'Please select a JSON file.'
    }
    return
  }

  isUploading.value = true
  uploadStatus.value = null

  try {
    const response = await api.uploadFile(file)
    uploadStatus.value = response
  } catch (error: any) {
    uploadStatus.value = {
      success: false,
      message: error.response?.data?.detail || 'Upload failed. Please try again.'
    }
  } finally {
    isUploading.value = false
  }
}

const resetUpload = () => {
  uploadStatus.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}
</script>

<style scoped>
.upload-area {
  transition: all 0.3s ease;
}

.upload-area:hover {
  @apply border-primary-400 bg-primary-25;
}

.upload-area.dragover {
  @apply border-primary-500 bg-primary-50 scale-105;
}
</style>
