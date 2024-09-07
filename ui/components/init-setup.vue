<template>
   <div
      class="d-flex flex-column justify-content-center align-items-center gap-1 vh-100 kontext-masthead"
   >
      <span class="d-flex align-items-center gap-1">
         <img :src="logo" alt="Kontext Logo" class="img-fluid" />
         <em class="kontext-em h5 mb-0 fw-bold">Copilot</em></span
      >
      <BCard title="" class="shadow-sm col-lg-6 mx-auto">
         <template #header>
            <div class="d-flex justify-content-between align-items-center">
               <h5>Loading</h5>
               <HelpMenu />
            </div>
         </template>
         <BCardText>
            <div
               v-if="settingsWrapper.isLoading"
               class="d-flex align-items-center gap-1"
            >
               <BSpinner variant="primary" />
               <span class="fw-bold">Loading settings ...</span>
            </div>
            <template v-else-if="settingsWrapper.error">
               <BAlert :model-value="true" variant="danger">
                  Error occurred while loading settings:
                  <b>{{ settingsWrapper.error }}</b> <br />
                  Please make sure backend services are running.</BAlert
               >
            </template>
            <template v-else-if="settingsWrapper.loaded">
               <div
                  v-if="!llmConnected && !stoppedTrying"
                  class="d-flex align-items-center gap-1"
               >
                  <BSpinner variant="primary" />
                  <span class="fw-bold">Fetching LLMs</span>
                  <span v-if="tries > 1" class="text-muted">
                     (attempt {{ tries }} / {{ maxTries }})</span
                  >
               </div>
               <BAlert
                  v-if="llmError"
                  class="my-1"
                  :model-value="true"
                  variant="danger"
               >
                  Error occurred while loading LLM model list:
                  <b> {{ llmError }}</b> <br />
                  Please make sure LLM service is running and the endpoint URL
                  is correct.
               </BAlert>
               <template v-if="!llmConnected && llmError">
                  <LlmEndpointSetting class="my-1" />
                  <BButton
                     v-if="stoppedTrying"
                     variant="primary"
                     class="mt-2"
                     :disabled="!stoppedTrying"
                     @click="tryFetchModels"
                  >
                     Retry
                  </BButton>
               </template>
            </template>
         </BCardText>
      </BCard>
   </div>
</template>
<script setup lang="ts">
import { BAlert } from "bootstrap-vue-next"
import logo from "~/assets/images/logo.svg"
import type { SettingsModelWrapper } from "~/types/Schemas"

const props = defineProps<{
   settingsWrapper: SettingsModelWrapper
}>()

const llmConnected = ref(false)
const llmError = ref("")

const { defaultModel, error, getModels } = useModels()

const tries = ref(0)
const maxTries = 10
const stoppedTrying = ref(false)

const emits = defineEmits(["llm-connected"])

const tryFetchModels = () => {
   tries.value = 0
   stoppedTrying.value = false
   const intervalId = setInterval(async () => {
      tries.value++
      await getModels()
      if (defaultModel.value) {
         llmConnected.value = true
         emits("llm-connected")
         clearInterval(intervalId)
      } else if (error.value) {
         llmError.value = error.value
      }
      if (tries.value >= maxTries) {
         clearInterval(intervalId)
         stoppedTrying.value = true
      }
   }, 2000)
}

watch(
   () => props.settingsWrapper.loaded,
   async (loaded) => {
      if (loaded && !defaultModel.value) {
         tryFetchModels()
      }
   },
   { immediate: false }
)
</script>
