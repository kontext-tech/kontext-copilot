<template>
    <NuxtLayout>
        <DefaultLayout>
            <template #["header-secondary"]>
                <OllamaModelSelector ref="modelSelector" />
            </template>

            <div class="px-4">
                <p class="text-muted">Generate embeddings from a model.
                </p>

                <div class="row d-flex gap-4">
                    <div class="col-md d-flex flex-column gap-4 mb-3">

                        <div class="col-md">
                            <label for="promptInput" class="form-label">Prompt</label>
                            <textarea class="form-control main-textarea" type="text" v-model="promptInput"
                                placeholder="Prompt template"></textarea>
                        </div>
                        <BButton button="primary" @click="generateResponse" :disabled="disableGenerate">Generate
                        </BButton>
                    </div>
                    <div class="col-md">
                        <label for="embeddings" class="form-label">Generated embeddings
                            <Spinner sm v-if="generating" text-color="success" />
                        </label>
                        <textarea class="form-control main-textarea" type="text" v-model="embeddings" :disabled="generating"></textarea>
                    </div>

                </div>

            </div>

        </DefaultLayout>
    </NuxtLayout>
</template>

<script setup lang="ts">
import DefaultLayout from '~/layouts/default-layout.vue'
import OllamaLlmService from '~/services/OllamaLlmService'

const modelSelector = ref()
const promptInput = ref<string>('')
const generating = ref<boolean>(false)
const embeddings = ref<string>('')

const { settings, isLoading, error, } = useSettings()
const ollamaService = new OllamaLlmService(settings.value.llm_endpoint)

const disableGenerate = computed(() => (promptInput.value ?? '').length === 0 || generating.value)

const generateResponse = async () => {
    generating.value = true
    ollamaService.ollama.embeddings({
        model: modelSelector.value?.selectedModelName,
        prompt: promptInput.value,
        options: { temperature: settings.value.llm_temperature, top_p: settings.value.llm_top_p, top_k: settings.value.llm_top_k, seed: settings.value.llm_seed },
    }).then((response) => {
        embeddings.value = JSON.stringify(response.embedding)
    }).finally(() => {
        generating.value = false
    })
}

</script>
