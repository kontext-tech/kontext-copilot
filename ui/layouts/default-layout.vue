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
               <div class="px-1 flex-shrink-0 border-top py-1">
                  <div class="d-flex align-items-center mx-2 gap-1">
                     <span
                        class="btn btn-circle btn-circle-nav btn-outline-secondary d-flex justify-content-center"
                     >
                        {{ initials }}
                     </span>
                     <span class="fw-bold">
                        {{ settings.generalUsername }}
                     </span>
                  </div>
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
               <div class="d-flex align-items-center gap-1 ms-auto">
                  <slot name="header-tools" />
                  <LlmSettingsButton />
                  <a
                     class="btn btn-sm btn-link"
                     :href="appConfig.kontextCopilotGitHubUrl"
                     target="_blank"
                  >
                     <Icon name="grommet-icons:github" size="18" />
                  </a>
                  <a
                     class="btn btn-sm btn-link"
                     :href="appConfig.kontextDiscordUrl"
                     target="_blank"
                  >
                     <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="18"
                        height="18"
                        fill="currentColor"
                        class="bi bi-discord"
                        viewBox="0 0 16 16"
                     >
                        <path
                           d="M13.545 2.907a13.2 13.2 0 0 0-3.257-1.011.05.05 0 0 0-.052.025c-.141.25-.297.577-.406.833a12.2 12.2 0 0 0-3.658 0 8 8 0 0 0-.412-.833.05.05 0 0 0-.052-.025c-1.125.194-2.22.534-3.257 1.011a.04.04 0 0 0-.021.018C.356 6.024-.213 9.047.066 12.032q.003.022.021.037a13.3 13.3 0 0 0 3.995 2.02.05.05 0 0 0 .056-.019q.463-.63.818-1.329a.05.05 0 0 0-.01-.059l-.018-.011a9 9 0 0 1-1.248-.595.05.05 0 0 1-.02-.066l.015-.019q.127-.095.248-.195a.05.05 0 0 1 .051-.007c2.619 1.196 5.454 1.196 8.041 0a.05.05 0 0 1 .053.007q.121.1.248.195a.05.05 0 0 1-.004.085 8 8 0 0 1-1.249.594.05.05 0 0 0-.03.03.05.05 0 0 0 .003.041c.24.465.515.909.817 1.329a.05.05 0 0 0 .056.019 13.2 13.2 0 0 0 4.001-2.02.05.05 0 0 0 .021-.037c.334-3.451-.559-6.449-2.366-9.106a.03.03 0 0 0-.02-.019m-8.198 7.307c-.789 0-1.438-.724-1.438-1.612s.637-1.613 1.438-1.613c.807 0 1.45.73 1.438 1.613 0 .888-.637 1.612-1.438 1.612m5.316 0c-.788 0-1.438-.724-1.438-1.612s.637-1.613 1.438-1.613c.807 0 1.451.73 1.438 1.613 0 .888-.631 1.612-1.438 1.612"
                        ></path>
                     </svg>
                  </a>
                  <HelpMenu />
                  <ThemeToggle simple />
               </div>
            </div>
            <div
               v-if="$slots['header-secondary']"
               class="header-secondary d-flex align-items-center border-bottom flex-shrink-0 px-4 d-grid gap-3 flex-wrap"
            >
               <slot name="header-secondary" />
            </div>
            <div
               class="flex-grow-1 flex-shrink-1 mw-100 w-100 d-flex flex-column overflow-y-auto default-area"
            >
               <div
                  v-if="$slots['secondary-sidebar']"
                  class="inset-0 h-100 row g-0"
               >
                  <div
                     class="col-md-8 col-lg-9 d-flex flex-column overflow-y-auto h-100"
                  >
                     <slot name="default" />
                  </div>
                  <div
                     class="col-md-4 col-lg-3 p-4 border-start d-none d-md-flex flex-column overflow-y-auto h-100"
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
