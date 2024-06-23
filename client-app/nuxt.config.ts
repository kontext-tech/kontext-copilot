import yaml from "@rollup/plugin-yaml"

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  ssr: false,
  vite: {
    plugins: [
      yaml(),
    ]
  },
  typescript: {
    strict: true,
    builder: 'vite',
    tsConfig: {
      compilerOptions: {
        target: 'esnext',
      }
    }
  },
  app:
  {
    baseURL: '/client/',
    head: {
      title: 'Kontext AI',
      link: [
        { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' },
      ]
    },
  },
  devServer: {
    port: 8080,
    host: 'localhost',
  },
  css: [
    '~/assets/scss/site.scss'
  ],

  modules: ["usebootstrap", '@nuxtjs/color-mode'],
  usebootstrap: {
    bootstrap: {
      prefix: ``
    },
    html: {
      prefix: `B`
    },
  },
  icon: {
    iconset: 'material-symbols',
    sizes: [16, 20, 24, 32, 48],
    defaultSize: 24
  },
  colorMode: {
    preference: 'system',
    fallback: 'light',
    hid: 'nuxt-color-mode-script',
    globalName: '__NUXT_COLOR_MODE__',
    componentName: 'ColorScheme',
    dataValue: 'bs-theme',
    storageKey: 'kontext-color-mode'
  }
});