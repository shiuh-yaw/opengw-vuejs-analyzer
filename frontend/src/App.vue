<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <!-- Navigation Header -->
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Logo and Title -->
          <div class="flex items-center space-x-4">
            <div class="flex-shrink-0">
              <h1 class="text-xl font-bold text-gray-900">
                OpenGW Agentic Analyzer
              </h1>
            </div>
            <div class="hidden md:block">
              <span class="text-sm text-gray-500">
                AI-Powered Transaction Analysis
              </span>
            </div>
          </div>

          <!-- Navigation Links -->
          <div class="hidden md:block">
            <div class="ml-10 flex items-baseline space-x-4">
              <RouterLink
                to="/"
                class="nav-link"
                :class="{ 'nav-link-active': $route.path === '/' }"
              >
                Dashboard
              </RouterLink>
              <RouterLink
                to="/upload"
                class="nav-link"
                :class="{ 'nav-link-active': $route.path === '/upload' }"
              >
                Upload
              </RouterLink>
              <RouterLink
                to="/transactions"
                class="nav-link"
                :class="{ 'nav-link-active': $route.path === '/transactions' }"
              >
                Transactions
              </RouterLink>
              <RouterLink
                to="/analysis"
                class="nav-link"
                :class="{ 'nav-link-active': $route.path === '/analysis' }"
              >
                Analysis
              </RouterLink>
            </div>
          </div>

          <!-- Mobile menu button -->
          <div class="md:hidden">
            <button
              @click="mobileMenuOpen = !mobileMenuOpen"
              class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
            >
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Mobile menu -->
        <div v-show="mobileMenuOpen" class="md:hidden">
          <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            <RouterLink
              to="/"
              class="mobile-nav-link"
              :class="{ 'mobile-nav-link-active': $route.path === '/' }"
              @click="mobileMenuOpen = false"
            >
              Dashboard
            </RouterLink>
            <RouterLink
              to="/upload"
              class="mobile-nav-link"
              :class="{ 'mobile-nav-link-active': $route.path === '/upload' }"
              @click="mobileMenuOpen = false"
            >
              Upload
            </RouterLink>
            <RouterLink
              to="/transactions"
              class="mobile-nav-link"
              :class="{ 'mobile-nav-link-active': $route.path === '/transactions' }"
              @click="mobileMenuOpen = false"
            >
              Transactions
            </RouterLink>
            <RouterLink
              to="/analysis"
              class="mobile-nav-link"
              :class="{ 'mobile-nav-link-active': $route.path === '/analysis' }"
              @click="mobileMenuOpen = false"
            >
              Analysis
            </RouterLink>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      <RouterView />
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-200 mt-auto">
      <div class="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center text-sm text-gray-500">
          <div>
            <span>OpenGW Agentic Analyzer</span>
            <span class="ml-2">v{{ $version }}</span>
          </div>
          <div>
            <span>Built: {{ formatBuildTime($buildTime) }}</span>
            <span class="ml-4">Cache: {{ $cacheBuster().slice(-8) }}</span>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'

const mobileMenuOpen = ref(false)

// Format build time for display
const formatBuildTime = (buildTime: string): string => {
  try {
    return new Date(buildTime).toLocaleString()
  } catch {
    return 'Unknown'
  }
}
</script>

<style scoped>
.nav-link {
  @apply text-gray-500 hover:text-gray-700 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200;
}

.nav-link-active {
  @apply text-primary-600 bg-primary-50;
}

.mobile-nav-link {
  @apply text-gray-500 hover:text-gray-700 block px-3 py-2 rounded-md text-base font-medium transition-colors duration-200;
}

.mobile-nav-link-active {
  @apply text-primary-600 bg-primary-50;
}
</style>
