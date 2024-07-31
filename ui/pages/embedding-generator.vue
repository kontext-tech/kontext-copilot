<template>
   <NuxtLayout>
      <DefaultLayout>
         <template #header-secondary>
            <LlmModelSelector ref="modelSelector" />
         </template>

         <div class="px-4 mt-3">
            <p class="text-muted">Generate embeddings from a model.</p>

            <div class="row d-flex gap-4">
               <div class="col-md d-flex flex-column gap-4 mb-3">
                  <div class="col-md">
                     <label for="promptInput" class="form-label">Prompt</label>
                     <textarea
                        v-model="promptInput"
                        class="form-control main-textarea"
                        type="text"
                        placeholder="Prompt template"
                     />
                  </div>
                  <BButton
                     variant="primary"
                     :disabled="disableGenerate"
                     @click="generateResponse"
                  >
                     Generate
                     <BSpinner v-if="generating" small />
                  </BButton>
               </div>
               <div class="col-md">
                  <label for="embeddings" class="form-label"
                     >Generated embeddings
                  </label>
                  <textarea
                     v-model="embeddings"
                     class="form-control main-textarea"
                     type="text"
                     :disabled="generating"
                  />
               </div>
            </div>
         </div>
      </DefaultLayout>
   </NuxtLayout>
</template>

<script setup lang="ts">
import DefaultLayout from "~/layouts/default-layout.vue"
import OllamaLlmService from "~/services/OllamaLlmService"
import type { SettingsWrapper } from "~/types/Schemas"

const modelSelector = ref()
const promptInput = ref<string>("")
const generating = ref<boolean>(false)
const embeddings = ref<string>("")

const settingsWrapper = inject("settings") as Ref<SettingsWrapper>
const settings = computed(() => settingsWrapper.value.settings)
const loaded = computed(() => settingsWrapper.value.loaded)

const disableGenerate = computed(
   () =>
      !loaded.value ||
      (promptInput.value ?? "").length === 0 ||
      generating.value
)
let ollamaService: OllamaLlmService

const getOllamaService = () => {
   if (!ollamaService && loaded.value) {
      ollamaService = new OllamaLlmService(
         settingsWrapper.value.settings.llm_endpoint
      )
   }
   return ollamaService
}

const generateResponse = async () => {
   generating.value = true
   const oService = getOllamaService()
   oService.ollama
      .embeddings({
         model: modelSelector.value?.selectedModelName,
         prompt: promptInput.value,
         options: {
            temperature: settings.value.llm_temperature,
            top_p: settings.value.llm_top_p,
            top_k: settings.value.llm_top_k,
            seed: settings.value.llm_seed
         }
      })
      .then((response) => {
         embeddings.value = JSON.stringify(response.embedding)
      })
      .finally(() => {
         generating.value = false
      })
}
</script>
