<template>
   <DefaultLayout>
      <div class="px-4 mt-3 w-100">
         <h1>Welcome!</h1>
         <div class="row row-cols-md-3 gap-3">
            <div class="col">
               <div class="card shadow-sm">
                  <div class="card-body">
                     <h5 class="card-title">Create a chat</h5>
                     <p class="text-muted">Initiate a chat with LLMs.</p>
                     <NuxtLink
                        to="/chat"
                        class="btn btn-outline-primary d-inline-flex gap-1 align-items-center"
                     >
                        <Icon name="material-symbols:edit-square-outline" />
                        <span>Start</span>
                     </NuxtLink>
                  </div>
               </div>
            </div>
         </div>
         <h4 class="my-3">About {{ appConfig.appName }}</h4>
         <BLink
            :href="appConfig.kontextCopilotUrl"
            class="btn btn-outline-primary"
            target="_blank"
         >
            Project site
         </BLink>
         <BLink
            :href="appConfig.kontextCopilotLinkedInUrl"
            class="btn btn-outline-primary ms-2"
            target="_blank"
         >
            Follow Kontext on LinkedIn
         </BLink>
      </div>
   </DefaultLayout>
</template>

<script setup lang="ts">
import appConfig from "~/app.config"
import DefaultLayout from "~/layouts/default-layout.vue"
usePageTitle()
</script>
