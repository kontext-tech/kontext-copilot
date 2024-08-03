<template>
   <NuxtLayout v-if="settingsWrapper.loaded">
      <NuxtPage />
   </NuxtLayout>
   <div
      v-else
      class="d-flex justify-content-center align-items-center gap-1 vh-100"
   >
      <BSpinner variant="primary" />
      <span class="fw-bold">Loading ...</span>
   </div>
</template>

<script setup lang="ts">
const { settingsWrapper } = useAppServices()
</script>
