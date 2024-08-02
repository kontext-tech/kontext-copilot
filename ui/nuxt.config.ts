const baseURL = "/ui/"
// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
   devtools: { enabled: false },
   ssr: false,

   typescript: {
      strict: true,
      builder: "vite",
      tsConfig: {
         compilerOptions: {
            target: "esnext"
         }
      }
   },

   app: {
      baseURL: baseURL,
      head: {
         title: "Kontext Copilot",
         htmlAttrs: {
            lang: "en"
         },
         link: [
            {
               rel: "icon",
               type: "image/svg+xml",
               href: `${baseURL}favicon.svg`
            }
         ]
      }
   },

   devServer: {
      port: 8101,
      host: "localhost"
   },

   modules: ["@nuxt/icon", "@bootstrap-vue-next/nuxt", "@nuxt/eslint"],

   css: ["~/assets/scss/site.scss"],

   runtimeConfig: {
      bootstrapVueNext: {
         composables: { useColorMode: false, all: false },
         directives: { all: false },
         css: true
      }
   },

   compatibilityDate: "2024-07-13"
})
