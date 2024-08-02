<template>
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
</template>

<script setup lang="ts">
import DefaultLayout from "~/layouts/default-layout.vue"

const modelSelector = ref()
const promptInput = ref<string>("")
const generating = ref<boolean>(false)
const embeddings = ref<string>("")

const settings = getSettings()

const disableGenerate = computed(
   () => (promptInput.value ?? "").length === 0 || generating.value
)
const llmService = getLlmService()

const generateResponse = async () => {
   if (!settings || !llmService.value) return
   generating.value = true
   llmService.value.ollama
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
