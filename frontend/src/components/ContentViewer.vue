<template>
  <div class="content-viewer">
    <!-- Content Type Toggle (only show if both JSON and XML exist) -->
    <div v-if="hasJson && hasXml" class="flex space-x-2 mb-4">
      <button
        @click="activeView = 'json'"
        :class="[
          'px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200',
          activeView === 'json'
            ? 'bg-blue-600 text-white shadow-md'
            : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
        ]"
      >
        <div class="flex items-center space-x-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
          </svg>
          <span>JSON</span>
        </div>
      </button>
      <button
        @click="activeView = 'xml'"
        :class="[
          'px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200',
          activeView === 'xml'
            ? 'bg-green-600 text-white shadow-md'
            : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
        ]"
      >
        <div class="flex items-center space-x-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
          </svg>
          <span>XML</span>
        </div>
      </button>
    </div>

    <!-- JSON Content -->
    <div v-if="hasJson && (activeView === 'json' || !hasXml)" class="content-section">
      <div class="flex items-center justify-between mb-3">
        <h4 class="text-sm font-semibold text-blue-700 flex items-center space-x-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
          </svg>
          <span>Beautified JSON</span>
        </h4>
        <div class="flex space-x-2">
          <button
            @click="copyToClipboard(jsonContent, 'JSON')"
            class="p-1 text-blue-600 hover:text-blue-800 transition-colors duration-200"
            title="Copy JSON"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
          </button>
          <button
            @click="toggleJsonCollapse"
            class="p-1 text-blue-600 hover:text-blue-800 transition-colors duration-200"
            :title="jsonCollapsed ? 'Expand JSON' : 'Collapse JSON'"
          >
            <svg class="w-4 h-4 transition-transform duration-200" :class="{ 'rotate-180': jsonCollapsed }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
        </div>
      </div>
      <div v-show="!jsonCollapsed" class="json-container">
        <pre class="json-content">{{ jsonContent }}</pre>
      </div>
    </div>

    <!-- XML Content -->
    <div v-if="hasXml && (activeView === 'xml' || !hasJson)" class="content-section">
      <div class="flex items-center justify-between mb-3">
        <h4 class="text-sm font-semibold text-green-700 flex items-center space-x-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
          </svg>
          <span>Beautified XML</span>
        </h4>
        <div class="flex space-x-2">
          <button
            @click="copyToClipboard(xmlContent, 'XML')"
            class="p-1 text-green-600 hover:text-green-800 transition-colors duration-200"
            title="Copy XML"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
          </button>
          <button
            @click="toggleXmlCollapse"
            class="p-1 text-green-600 hover:text-green-800 transition-colors duration-200"
            :title="xmlCollapsed ? 'Expand XML' : 'Collapse XML'"
          >
            <svg class="w-4 h-4 transition-transform duration-200" :class="{ 'rotate-180': xmlCollapsed }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
        </div>
      </div>
      <div v-show="!xmlCollapsed" class="xml-container">
        <pre class="xml-content">{{ xmlContent }}</pre>
      </div>
    </div>

    <!-- No Content Message -->
    <div v-if="!hasJson && !hasXml" class="no-content">
      <div class="text-center py-8 text-gray-500">
        <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <p class="text-lg font-medium text-gray-900 mb-2">No Structured Content</p>
        <p class="text-gray-600">This log entry does not contain JSON or XML data.</p>
      </div>
    </div>

    <!-- Copy Success Toast -->
    <div
      v-if="showCopySuccess"
      class="fixed bottom-4 right-4 bg-green-600 text-white px-4 py-2 rounded-lg shadow-lg transition-all duration-300 z-50"
    >
      <div class="flex items-center space-x-2">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        <span>{{ copySuccessMessage }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

// Props
interface Props {
  jsonContent?: string
  xmlContent?: string
  defaultView?: 'json' | 'xml'
}

const props = withDefaults(defineProps<Props>(), {
  defaultView: 'json'
})

// Reactive data
const activeView = ref<'json' | 'xml'>(props.defaultView)
const jsonCollapsed = ref(false)
const xmlCollapsed = ref(false)
const showCopySuccess = ref(false)
const copySuccessMessage = ref('')

// Computed properties
const hasJson = computed(() => Boolean(props.jsonContent))
const hasXml = computed(() => Boolean(props.xmlContent))

// Watch for prop changes to reset active view
watch([() => props.jsonContent, () => props.xmlContent], () => {
  if (hasJson.value && !hasXml.value) {
    activeView.value = 'json'
  } else if (hasXml.value && !hasJson.value) {
    activeView.value = 'xml'
  } else if (hasJson.value && hasXml.value) {
    activeView.value = props.defaultView
  }
})

// Methods
const toggleJsonCollapse = () => {
  jsonCollapsed.value = !jsonCollapsed.value
}

const toggleXmlCollapse = () => {
  xmlCollapsed.value = !xmlCollapsed.value
}

const copyToClipboard = async (content: string, type: string) => {
  try {
    await navigator.clipboard.writeText(content)
    copySuccessMessage.value = `${type} copied to clipboard!`
    showCopySuccess.value = true
    
    setTimeout(() => {
      showCopySuccess.value = false
    }, 3000)
  } catch (err) {
    console.error('Failed to copy to clipboard:', err)
    // Fallback for older browsers
    const textArea = document.createElement('textarea')
    textArea.value = content
    document.body.appendChild(textArea)
    textArea.select()
    document.execCommand('copy')
    document.body.removeChild(textArea)
    
    copySuccessMessage.value = `${type} copied to clipboard!`
    showCopySuccess.value = true
    
    setTimeout(() => {
      showCopySuccess.value = false
    }, 3000)
  }
}
</script>

<style scoped>
.content-section {
  @apply border border-gray-200 rounded-lg overflow-hidden;
}

.json-container {
  @apply bg-blue-50 border-t border-blue-200;
}

.xml-container {
  @apply bg-green-50 border-t border-green-200;
}

.json-content {
  @apply p-4 text-sm text-blue-900 font-mono leading-relaxed overflow-x-auto;
  font-family: 'JetBrains Mono', 'Courier New', monospace;
  white-space: pre-wrap;
  word-break: break-word;
}

.xml-content {
  @apply p-4 text-sm text-green-900 font-mono leading-relaxed overflow-x-auto;
  font-family: 'JetBrains Mono', 'Courier New', monospace;
  white-space: pre-wrap;
  word-break: break-word;
}

.no-content {
  @apply border border-gray-200 rounded-lg bg-gray-50;
}

/* Syntax highlighting for JSON */
.json-content {
  color: #1e40af;
}

/* Syntax highlighting for XML */
.xml-content {
  color: #166534;
}

/* Custom scrollbar for code blocks */
.json-content::-webkit-scrollbar,
.xml-content::-webkit-scrollbar {
  height: 8px;
  width: 8px;
}

.json-content::-webkit-scrollbar-track,
.xml-content::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

.json-content::-webkit-scrollbar-thumb {
  background: rgba(37, 99, 235, 0.3);
  border-radius: 4px;
}

.xml-content::-webkit-scrollbar-thumb {
  background: rgba(22, 101, 52, 0.3);
  border-radius: 4px;
}

.json-content::-webkit-scrollbar-thumb:hover {
  background: rgba(37, 99, 235, 0.5);
}

.xml-content::-webkit-scrollbar-thumb:hover {
  background: rgba(22, 101, 52, 0.5);
}
</style>
