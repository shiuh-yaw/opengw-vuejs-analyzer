import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '@/views/DashboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView,
      meta: {
        title: 'Dashboard - OpenGW Agentic Analyzer'
      }
    },
    {
      path: '/upload',
      name: 'upload',
      component: () => import('@/views/UploadView.vue'),
      meta: {
        title: 'Upload - OpenGW Agentic Analyzer'
      }
    },
    {
      path: '/transactions',
      name: 'transactions',
      component: () => import('@/views/TransactionsView.vue'),
      meta: {
        title: 'Transactions - OpenGW Agentic Analyzer'
      }
    },
    {
      path: '/analysis',
      name: 'analysis',
      component: () => import('@/views/AnalysisView.vue'),
      meta: {
        title: 'Analysis - OpenGW Agentic Analyzer'
      }
    },
    {
      path: '/transaction/:id',
      name: 'transaction-detail',
      component: () => import('@/views/TransactionDetailView.vue'),
      meta: {
        title: 'Transaction Detail - OpenGW Agentic Analyzer'
      }
    }
  ]
})

// Add cache prevention to route changes
router.beforeEach((to, from, next) => {
  // Update document title
  if (to.meta?.title) {
    document.title = to.meta.title as string
  }
  
  // Add cache buster to route
  const cacheBuster = `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
  
  // Add cache prevention meta tag
  let metaTag = document.querySelector('meta[name="route-cache-buster"]')
  if (!metaTag) {
    metaTag = document.createElement('meta')
    metaTag.setAttribute('name', 'route-cache-buster')
    document.head.appendChild(metaTag)
  }
  metaTag.setAttribute('content', cacheBuster)
  
  next()
})

export default router
