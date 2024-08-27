<template>
   <DefaultLayout>
      <div class="px-4 mt-3 w-100 row row-cols-md-2">
         <div class="col">
            <div class="card">
               <div class="card-body">
                  <h5 class="card-title">
                     <Icon
                        name="material-symbols:lightbulb-outline"
                        size="24"
                     ></Icon>
                     Prompt scratchboard
                  </h5>
                  <p class="text-muted">Write and test prompts with LLMs.</p>
                  <NuxtLink
                     to="/prompt-engineering"
                     class="btn btn-outline-primary d-inline-flex gap-1 align-items-center"
                  >
                     Try</NuxtLink
                  >
               </div>
            </div>
         </div>
         <div class="col">
            <div class="card">
               <div class="card-body">
                  <h5 class="card-title">
                     <Icon name="material-symbols:transform" size="24"></Icon>
                     Embedding generator
                  </h5>
                  <p class="text-muted">Generate embeddings from a model.</p>
                  <NuxtLink
                     to="/embedding-generator"
                     class="btn btn-outline-primary d-inline-flex gap-1 align-items-center"
                  >
                     Try</NuxtLink
                  >
               </div>
            </div>
         </div>
      </div>
   </DefaultLayout>
</template>

<script setup lang="ts">
import DefaultLayout from "~/layouts/default-layout.vue"
usePageTitle()
</script>
