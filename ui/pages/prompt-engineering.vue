<template>
   <DefaultLayout>
      <template #header-secondary>
         <LlmModelSelector ref="modelSelector" />
         <LlmSettingsButton />
         <BFormCheckbox
            v-model="streaming"
            switch
            class="d-flex align-items-center gap-1"
         >
            Streaming
         </BFormCheckbox>
         <BFormCheckbox
            v-model="jsonFormat"
            switch
            class="d-flex align-items-center gap-1"
         >
            JSON format
         </BFormCheckbox>
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
               <label for="userInput" class="form-label">Response </label>
               <textarea
                  v-model="state.currentResponse.content"
                  class="form-control main-textarea"
                  type="text"
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
import type { PromptInfo, Prompt } from "~/types/Schemas"
const streaming = ref(true)
const jsonFormat = ref<boolean>(false)
const modelSelector = ref()
const systemPromptInput = ref<string>()
const promptInput = ref<string>("")
const userInput = ref<string>()

const llmClient = getLlmClientService()
const state = llmClient.state
const promptService = getPromptService()

const selectedTemplateId = ref(null)
const promptTemplates = ref<PromptInfo[]>([])
const promptTemplate = ref<Prompt | null>(null)

const disableGenerate = computed(
   () => (promptInput.value ?? "").length === 0 || state.generating
)
const jsonOption = computed(() => (jsonFormat.value ? "json" : ""))

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
   if (userInput.value)
      llmClient.generate(
         promptInput.value,
         userInput.value,
         modelSelector.value?.selectedModelName,
         jsonOption.value,
         streaming.value,
         undefined,
         systemPromptInput.value
      )
}

const loadPromptTemplate = async (template_id: string) => {
   promptTemplate.value = await promptService.getPromptTemplate(template_id)
   if (promptTemplate.value) {
      systemPromptInput.value = promptTemplate.value.system_prompt
      promptInput.value = promptTemplate.value.prompt
      userInput.value = promptTemplate.value.user_input
      generateResponse()
   }
}

usePageTitle()
</script>
