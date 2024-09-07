<template>
   <NuxtLayout v-if="ready">
      <NuxtPage />
   </NuxtLayout>
   <InitSetup
      v-else
      ref="init"
      :settings-wrapper="settingsWrapper"
      @llm-connected="handleLlmConnected"
   />
</template>

<script setup lang="ts">
import InitSetup from "./components/init-setup.vue"

const init = ref<InstanceType<typeof InitSetup>>()
const { settingsWrapper } = useAppServices()
const llmConnected = ref(false)

const handleLlmConnected = () => {
   llmConnected.value = true
}

const ready = computed(() => settingsWrapper.loaded && llmConnected.value)
</script>
