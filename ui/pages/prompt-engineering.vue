<template>
   <NuxtLayout>
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

            <div v-if="loaded" class="row d-flex gap-4">
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
                     <label for="userInput" class="form-label"
                        >User input</label
                     >
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
                     <BSpinner v-if="generating" small />
                  </BButton>
               </div>
               <div class="col-md">
                  <label for="userInput" class="form-label">Response </label>
                  <textarea
                     v-model="response"
                     class="form-control main-textarea"
                     type="text"
                     placeholder="Generated response"
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
import { PromptsService } from "~/services/ApiServices"
import OllamaLlmService from "~/services/OllamaLlmService"
import type { PromptInfo, Prompt, SettingsWrapper } from "~/types/Schemas"
const streaming = ref(true)
const jsonFormat = ref<boolean>(false)
const modelSelector = ref()
const systemPromptInput = ref<string>()
const promptInput = ref<string>("")
const userInput = ref<string>()
const response = ref<string>()
const generating = ref<boolean>(false)

const settingsWrapper = inject("settings") as Ref<SettingsWrapper>
const settings = computed(() => settingsWrapper.value.settings)
const loaded = computed(() => settingsWrapper.value.loaded)

const selectedTemplateId = ref(null)
const promptTemplates = ref<PromptInfo[]>([])
const promptTemplate = ref<Prompt | null>(null)

const disableGenerate = computed(
   () => (promptInput.value ?? "").length === 0 || generating.value
)
const jsonOption = computed(() => (jsonFormat.value ? "json" : ""))
const appConfig = useAppConfig()
const promptService = new PromptsService(appConfig.apiBaseUrl)

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
   response.value = ""
   let prompt_str = promptInput.value
   /* Replace {{$input}} with user input */
   if (userInput.value) {
      prompt_str = prompt_str.replace(/\{\{\$input\}\}/g, userInput.value)
   }
   const oService = getOllamaService()

   if (streaming.value) {
      const res = await oService.ollama.generate({
         model: modelSelector.value?.selectedModelName,
         prompt: prompt_str,
         system: systemPromptInput.value,
         format: jsonOption.value,
         stream: true,
         options: {
            temperature: settings.value.llm_temperature,
            top_p: settings.value.llm_top_p,
            top_k: settings.value.llm_top_k,
            seed: settings.value.llm_seed
         }
      })
      for await (const part of res) {
         // Append the response to the response textarea
         if (response.value) response.value += part.response
         else response.value = part.response

         if (part.done) {
            generating.value = false
         }
      }
   } else {
      const res = await oService.ollama.generate({
         model: modelSelector.value?.selectedModelName,
         prompt: prompt_str,
         system: systemPromptInput.value,
         stream: false,
         format: jsonOption.value,
         options: {
            temperature: settings.value.llm_temperature,
            top_p: settings.value.llm_top_p,
            top_k: settings.value.llm_top_k,
            seed: settings.value.llm_seed
         }
      })
      response.value = res.response
      generating.value = false
   }
}

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
