// Global build-time constants
declare const __BUILD_TIME__: string
declare const __VERSION__: string

// Vue global properties
declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $buildTime: string
    $version: string
    $cacheBuster: () => string
  }
}

export {}
