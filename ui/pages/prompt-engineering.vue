<template>
   <DefaultLayout>
      <template #header-secondary>
         <LlmSettingsToolbar
            v-model="llmToolbar"
            settings-button
            streaming-toggle
            json-toogle
            :streaming-default="true"
         />
      </template>

      <template #header-tools>
         <LlmModelSelector simple />
      </template>

      <div class="px-4 mt-3">
         <p class="text-muted">
            Test your prompts with this utility or select examples from the
            dropdown list to get started.
         </p>

         <div v-if="llmClient" class="row d-flex gap-4">
            <div
               class="col-md d-flex flex-column gap-4 justify-content-center mb-3"
            >
               <div class="col-md">
                  <BFormSelect
                     v-model="selectedTemplateId"
                     aria-label="Select prompt template"
                     class="col-md"
                  >
                     <BFormSelectOption selected value="null">
                        Select prompt template
                     </BFormSelectOption>
                     <BFormSelectOption
                        v-for="template in promptTemplates"
                        :key="template.id"
                        :value="template.id"
                     >
                        {{ template.name }}
                     </BFormSelectOption>
                  </BFormSelect>
               </div>
               <div class="col-md">
                  <label for="systemPromptInput" class="form-label"
                     >System prompt</label
                  >
                  <textarea
                     v-model="systemPromptInput"
                     class="form-control main-textarea"
                     type="text"
                     placeholder="System prompt"
                  />
               </div>
               <div class="col-md">
                  <label for="promptInput" class="form-label">Prompt</label>
                  <textarea
                     v-model="promptInput"
                     class="form-control main-textarea"
                     type="text"
                     placeholder="Prompt template"
                  />
               </div>
               <div class="col-md">
                  <label for="userInput" class="form-label">User input</label>
                  <span v-pre class="text-muted ms-1"
                     >(Placeholder {{ $input }} in your prompt.)</span
                  >
                  <textarea
                     v-model="userInput"
                     class="form-control main-textarea"
                     type="text"
                     placeholder="User input"
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
               <label for="userInput" class="form-label">Response </label>
               <textarea
                  v-model="state.generatedContent"
                  class="form-control main-textarea"
                  type="text"
                  rows="8"
                  placeholder="Generated response"
                  :disabled="state.generating"
               />
            </div>
         </div>
      </div>
   </DefaultLayout>
</template>

<script setup lang="ts">
import DefaultLayout from "~/layouts/default-layout.vue"
import { LlmModelRequiredException } from "~/types/Errors"
import type {
   LlmToolbarOptions,
   PromptInfoModel,
   PromptModel
} from "~/types/Schemas"

const llmToolbar = reactive<LlmToolbarOptions>({
   streaming: false,
   format: ""
})

const systemPromptInput = ref<string>()
const promptInput = ref<string>("")
const userInput = ref<string>()

const llmClient = getCopilotClientService()
const state = llmClient.state
const promptService = getPromptService()

const selectedTemplateId = ref(null)
const promptTemplates = ref<PromptInfoModel[]>([])
const promptTemplate = ref<PromptModel | null>(null)

const disableGenerate = computed(
   () => (promptInput.value ?? "").length === 0 || state.generating
)

onMounted(async () => {
   promptTemplates.value = await promptService.getPromptTemplates()
})

watch(
   () => selectedTemplateId.value,
   async (template_id) => {
      if (template_id) {
         await loadPromptTemplate(template_id)
      }
   }
)

const generateResponse = async () => {
   if (!llmToolbar.model) throw new LlmModelRequiredException()

   if (userInput.value)
      llmClient.generate(
         promptInput.value,
         userInput.value,
         llmToolbar.model,
         llmToolbar.format,
         llmToolbar.streaming,
         undefined,
         systemPromptInput.value
      )
}

const loadPromptTemplate = async (template_id: string) => {
   promptTemplate.value = await promptService.getPromptTemplate(template_id)
   if (promptTemplate.value) {
      systemPromptInput.value = promptTemplate.value.systemPrompt
      promptInput.value = promptTemplate.value.prompt
      userInput.value = promptTemplate.value.userInput
      generateResponse()
   }
}

usePageTitle()
</script>
