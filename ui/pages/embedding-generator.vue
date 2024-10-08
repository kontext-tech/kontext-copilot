<template>
   <DefaultLayout>
      <template #header-tools>
         <LlmModelSelector simple />
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
                     rows="16"
                     placeholder="Prompt template"
                  />
               </div>
               <div>
                  <BButton
                     variant="primary"
                     :disabled="disableGenerate"
                     @click="generateResponse"
                  >
                     Generate
                     <BSpinner v-if="state.generating" small />
                  </BButton>
               </div>
            </div>
            <div class="col-md">
               <label for="embeddings" class="form-label"
                  >Generated embeddings
               </label>
               <textarea
                  v-model="generatedState.embeddings"
                  class="form-control main-textarea"
                  type="text"
                  rows="16"
                  :disabled="state.generating"
               />
               <div class="mt-3">
                  <label>Length: </label>
                  <b class="ms-1">{{ state.generatedEmbeddings?.length }}</b>
               </div>
            </div>
         </div>
      </div>
   </DefaultLayout>
</template>

<script setup lang="ts">
import DefaultLayout from "~/layouts/default-layout.vue"
import { LlmModelRequiredException } from "~/types/Errors"

const promptInput = ref<string>("")

const llmClient = getCopilotClientService()
const state = llmClient.state

const disableGenerate = computed(
   () => (promptInput.value ?? "").length === 0 || state.generating
)

const generatedState = reactive({ embeddings: "" })

const { defaultModel } = useModels()

const generateResponse = async () => {
   if (!defaultModel.value?.name) throw new LlmModelRequiredException()
   llmClient
      .embeddings(promptInput.value, defaultModel.value?.name)
      .then(() => {
         generatedState.embeddings = JSON.stringify(state.generatedEmbeddings)
      })
}

usePageTitle()
</script>
