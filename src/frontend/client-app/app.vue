<template>
  <NuxtLayout>
    <DefaultLayout>
      <template #main>
        <NuxtPage />
      </template>
      <template #aside>
      </template>
    </DefaultLayout>
  </NuxtLayout>
</template>

<script setup lang="ts">
import DefaultLayout from './layouts/default-layout.vue'
</script>

<style scoped></style>