import yaml from "@rollup/plugin-yaml";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },

  vite: {
    plugins: [
      yaml()
    ]
  },

  app:
  {
    head: {
      title: 'Kontext AI',
      link: [
        { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' },
      ]
    }
  },

  css: [
    '~/scss/site.scss'
  ],

  modules: ["usebootstrap"],
  usebootstrap: {
    bootstrap: {
      prefix: `k-`
    },
    html: {
      prefix: `B`
    },
  },
  icon: {
    iconset: 'material-symbols',
    sizes: [16, 20, 24, 32, 48],
    defaultSize: 24
  }
});