import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// Cache prevention: Add build time and version to document
document.documentElement.setAttribute('data-build-time', __BUILD_TIME__)
document.documentElement.setAttribute('data-version', __VERSION__)

// Add cache-busting meta tag
const metaTag = document.createElement('meta')
metaTag.setAttribute('name', 'cache-buster')
metaTag.setAttribute('content', `${Date.now()}-${Math.random()}`)
document.head.appendChild(metaTag)

const app = createApp(App)

// Global properties for cache prevention
app.config.globalProperties.$buildTime = __BUILD_TIME__
app.config.globalProperties.$version = __VERSION__
app.config.globalProperties.$cacheBuster = () => `${Date.now()}-${Math.random()}`

app.use(createPinia())
app.use(router)

app.mount('#app')
