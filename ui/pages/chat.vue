<template>
   <DefaultLayout>
      <template #header-secondary>
         <LlmSettingsToolbar
            id="llmToolbar"
            ref="llmToolbar"
            model-selector
            settings-button
            streaming-toggle
            :streaming-default="true"
         />
      </template>

      <ChatMainWindow
         v-model:session-title="sessionTitle"
         :model="selectedModelName"
         class="mt-3 px-4"
      />
   </DefaultLayout>
</template>

<script setup lang="ts">
import LlmSettingsToolbar from "~/components/llm/settings-toolbar.vue"
import DefaultLayout from "~/layouts/default-layout.vue"

const llmToolbar = ref<InstanceType<typeof LlmSettingsToolbar> | null>(null)
const selectedModelName = computed(() => llmToolbar.value?.model)

const sessionTitle = ref<string>("General chat")

usePageTitle()
</script>
