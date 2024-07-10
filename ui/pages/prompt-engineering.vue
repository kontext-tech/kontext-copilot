<template>
    <NuxtLayout>
        <DefaultLayout>
            <template #["header-secondary"]>
                <OllamaModelSelector ref="modelSelector" />
                <BButton button="outline-primary" toggle="modal" target="#llmsSettingsModal" class="d-flex align-items-center">
                    <Icon name="material-symbols:neurology-outline" size="20" /> LLMs settings
                </BButton>
                <Modal id="llmsSettingsModal">
                    <ModalDialog class="modal-lg">
                        <ModalContent>
                            <ModalHeader>
                                <ModalTitle>LLMs settings</ModalTitle>
                                <CloseButton dismiss="modal" />
                            </ModalHeader>
                            <ModalBody>
                                <LlmSettings />
                            </ModalBody>
                            <ModalFooter>
                                <BButton button="secondary" dismiss="modal">
                                    Close
                                </BButton>
                            </ModalFooter>
                        </ModalContent>
                    </ModalDialog>
                </Modal>
                <BFormCheck switch class="d-flex align-items-center gap-1">
                    <BFormCheckInput v-model="streaming" />
                    <BFormCheckLabel>Streaming</BFormCheckLabel>
                </BFormCheck>
                <BFormCheck switch class="d-flex align-items-center gap-1">
                    <BFormCheckInput v-model="jsonFormat" />
                    <BFormCheckLabel>JSON format</BFormCheckLabel>
                </BFormCheck>
            </template>

            <div class="px-4">
                <p class="text-muted">Test your prompts with this utility or select examples from the dropdown list to
                    get started.
                </p>

                <div class="row d-flex gap-4">
                    <div class="col-md d-flex flex-column gap-4 justify-content-center mb-3">
                        <div class="col-md">
                            <BFormSelect v-model="selectedTemplateId" aria-label="Select prompt template"
                                class="col-md">
                                <b-option selected>
                                    Select prompt template
                                </b-option>
                                <b-option v-for="template in promptTemplates" :key="template.id" :value="template.id">
                                    {{ template.name }}
                                </b-option>
                            </BFormSelect>
                        </div>
                        <div class="col-md">
                            <label for="systemPromptInput" class="form-label">System prompt</label>
                            <textarea class="form-control main-textarea" type="text" v-model="systemPromptInput"
                                placeholder="System prompt"></textarea>
                        </div>
                        <div class="col-md">
                            <label for="promptInput" class="form-label">Prompt</label>
                            <textarea class="form-control main-textarea" type="text" v-model="promptInput"
                                placeholder="Prompt template"></textarea>
                        </div>
                        <div class="col-md">
                            <label for="userInput" class="form-label">User input</label>
                            <span class="text-muted ms-1" v-pre>(Placeholder {{$input}} in your prompt.)</span>
                            <textarea class="form-control main-textarea" type="text" v-model="userInput"
                                placeholder="User input"></textarea>
                        </div>

                        <BButton button="primary" @click="generateResponse"
                            :disabled="disableGenerate">Generate</BButton>
                    </div>
                    <div class="col-md">
                        <label for="userInput" class="form-label">Response <Spinner sm v-if="generating" text-color="success" /></label>
                        <textarea class="form-control main-textarea" type="text" v-model="response"
                            placeholder="Generated response" :disabled="generating"></textarea>
                    </div>

                </div>

            </div>

        </DefaultLayout>
    </NuxtLayout>
</template>

<script setup lang="ts">
import { set } from 'lodash';
import DefaultLayout from '~/layouts/default-layout.vue'
import { PromptsService } from '~/services/ApiServices'
import OllamaLlmService from '~/services/OllamaLlmService'
import type { PromptInfo, Prompt } from '~/types/Schemas'
const streaming = ref(true)
const jsonFormat = ref<boolean>(false)
const modelSelector = ref()
const systemPromptInput = ref<string>()
const promptInput = ref<string>('')
const userInput = ref<string>()
const response = ref<string>()
const generating = ref<boolean>(false)

const { settings, isLoading, error, } = useSettings()

const selectedTemplateId = ref()
const promptTemplates = ref<PromptInfo[]>([])
const promptTemplate = ref<Prompt | null>(null)

const disableGenerate = computed(() => (promptInput.value ?? '').length === 0 || generating.value)
const jsonOption = computed(() => jsonFormat.value ? 'json' : '')

const service = new OllamaLlmService(settings.value.llm_endpoint)
const promptService = new PromptsService()

const generateResponse = async () => {
    generating.value = true
    response.value = ''
    let prompt_str = promptInput.value
    /* Replace {{$input}} with user input */
    if (userInput.value) {
        prompt_str = prompt_str.replace(/\{\{\$input\}\}/g, userInput.value)
    }

    if (streaming.value) {
        const res = await service.ollama.generate({
            model: modelSelector.value?.selectedModelName,
            prompt: prompt_str,
            system: systemPromptInput.value,
            format: jsonOption.value,
            stream: true,
            options: { temperature: settings.value.llm_temperature, top_p: settings.value.llm_top_p, top_k: settings.value.llm_top_k, seed: settings.value.llm_seed },

        })
        for await (const part of res) {
            // Append the response to the response textarea
            if (response.value)
                response.value += part.response
            else
                response.value = part.response

            if (part.done) {
                generating.value = false
            }
        }

    } else {
        const res = await service.ollama.generate({
            model: modelSelector.value?.selectedModelName,
            prompt: prompt_str,
            system: systemPromptInput.value,
            stream: false,
            format: jsonOption.value,
            options: { temperature: settings.value.llm_temperature, top_p: settings.value.llm_top_p, top_k: settings.value.llm_top_k, seed: settings.value.llm_seed },

        })
        response.value = res.response
        generating.value = false
    }
}

onMounted(async () => {
    promptTemplates.value = await promptService.getPromptTemplates()
})

watch(() => selectedTemplateId.value, async (template_id) => {
    if (template_id) {
        await loadPromptTemplate(template_id)
    }
})

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
