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
                  <BSpinner v-if="state.generating" small />
               </BButton>
            </div>
            <div class="col-md">
               <label for="embeddings" class="form-label"
                  >Generated embeddings
               </label>
               <textarea
                  v-model="state.currentResponse.content"
                  class="form-control main-textarea"
                  type="text"
                  :disabled="state.generating"
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

const llmClient = getLlmClientService()
const state = llmClient.state

const disableGenerate = computed(
   () => (promptInput.value ?? "").length === 0 || state.generating
)

const generateResponse = async () => {
   llmClient.embeddings(
      promptInput.value,
      modelSelector.value?.selectedModelName
   )
}
</script>
