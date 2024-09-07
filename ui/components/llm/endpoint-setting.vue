<template>
   <div class="d-flex justify-content-between align-items-center">
      <div class="col-md-8">
         <h6>Ollama Endpoint</h6>
         <span class="text-muted">The endpoint for Ollama.</span>
      </div>
      <div class="col-md-4">
         <BFormInput id="endpointOllama" v-model="settings.llmOllamaEndpoint" />
      </div>
   </div>
</template>
<script setup lang="ts">
const settings = getSettings()
</script>
