<template>
   <div
      class="position-fixed d-flex overflow-x-hidden overflow-y-hidden inset-0 w-100"
   >
      <BCollapse
         id="mainSidebar"
         class="position-relative-md sidebar-col d-md-flex flex-column align-items-stretch offcanvas-md offcanvas-start border-end flex-shrink-0 bg-body shadow-sm"
      >
         <div
            class="px-4 header-primary d-flex align-items-center flex-shrink-0 border-bottom bg-body-tertiary shadow-sm"
         >
            <BLink
               v-b-toggle.mainSidebar
               class="d-flex d-md-none text-muted me-3"
               href="#"
            >
               <Icon name="material-symbols:menu" size="24" />
            </BLink>
            <a href="/" class="navbar-brand">
               <span class="d-flex align-items-center gap-1">
                  <img :src="logo" alt="Kontext Logo" class="img-fluid" />
                  <em class="kontext-em h5 mb-0 fw-bold">Copilot</em></span
               >
            </a>
         </div>
         <div
            class="d-flex flex-column w-100 flex-grow-1 flex-shrink-1 position-relative overflow-y-hidden"
         >
            <div class="flex-grow-1 d-flex flex-column min-h-0">
               <div class="overflow-y-auto flex-grow-1 flex-shrink-1">
                  <SidebarPanel class="flex-grow-1 flex-shrink-1" />
                  <div class="flex-grow-1 flex-shrink-1">
                     <slot name="aside" />
                  </div>
               </div>
               <div
                  class="px-1 text-center d-flex flex-shrink-0 align-items-center border-top py-1 gap-1"
               >
                  <span
                     class="btn btn-circle btn-circle-nav btn-outline-secondary d-flex align-items-center justify-content-center"
                  >
                     {{ initials }}
                  </span>
                  <span class="fw-bold">
                     {{ settings.generalUsername }}
                  </span>
               </div>
            </div>
         </div>
      </BCollapse>
      <div class="d-flex flex-grow-1 flex-shrink-1 w-100">
         <div
            class="flex-column align-items-stretch position-relative w-100 flex-grow-1 flex-shrink-1 d-flex"
         >
            <div
               class="header-primary d-flex align-items-center border-bottom px-4 flex-shrink-0"
            >
               <BLink
                  v-b-toggle.mainSidebar
                  class="d-flex d-md-none text-muted me-3"
                  href="#"
               >
                  <Icon name="material-symbols:menu" size="24" />
               </BLink>
               <h1 class="fs-6 mb-0 pb-0 fw-bold">
                  {{ route.meta["title"] ?? route.name }}
               </h1>
               <ThemeToggle class="ms-auto" simple />
            </div>
            <div
               v-if="$slots['header-secondary']"
               class="header-secondary d-flex align-items-center border-bottom flex-shrink-0 px-4 d-grid gap-3 flex-wrap"
            >
               <slot name="header-secondary" />
            </div>
            <div
               class="flex-grow-1 flex-shrink-1 d-flex flex-column overflow-y-auto default-area"
            >
               <div
                  v-if="$slots['secondary-sidebar']"
                  class="d-flex w-100 inset-0 h-100"
               >
                  <div
                     class="flex-grow-1 flex-shrink-1 d-flex flex-column overflow-y-auto col-md-8 col-lg-9 h-100"
                  >
                     <slot name="default" />
                  </div>
                  <div
                     class="flex-shrink-0 secondary-sidebar border-start d-none d-md-flex flex-column overflow-y-auto col-md-4 col-lg-3 p-4 h-100"
                  >
                     <slot name="secondary-sidebar" />
                  </div>
               </div>
               <div
                  v-else
                  class="flex-grow-1 flex-shrink-1 d-flex flex-column overflow-y-auto"
               >
                  <slot name="default" />
               </div>
            </div>
         </div>
      </div>
   </div>
</template>

<script setup lang="ts">
import logo from "~/assets/images/logo.svg"

const route = useRoute()
const appConfig = useAppConfig()

const settings = getSettings()

const initials = computed(() => {
   return settings.value.generalUsername
      .split(" ")
      .map((n) => n[0])
      .join("")
})

watchEffect(() => {
   useHead({
      title: route.meta["title"] || appConfig.appName
   })
})
</script>

<style scoped></style>
