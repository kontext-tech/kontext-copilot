import type { ModelResponse } from "ollama/browser"
import OllamaLlmService from "~/services/OllamaLlmService"

export default function useOllamaModels() {
    const models = ref<ModelResponse[]>([])

    const defaultModel = ref<ModelResponse>()

    const { settings, loaded } = useSettings()
    const defaultModelConfig = computed(() => settings.value.llm_default_model)
    let ollamaService: OllamaLlmService


    const getModels = async () => {
        if (!ollamaService) return
        const response = await ollamaService.getModels()
        models.value = response.models
        const model = models.value.find(model => model.name === defaultModelConfig.value)
        if (model)
            defaultModel.value = model
        else
            defaultModel.value = models.value[0]
    }

    watch(loaded, async (value) => {
        if (value) {
            ollamaService = new OllamaLlmService(settings.value.llm_endpoint)
            await getModels()
        }
    })

    /* persist default model selection to local storage */
    const setDefaultModel = (model: ModelResponse) => {
        defaultModel.value = model
        settings.value.llm_default_model = model.name
    }

    return { models, defaultModel, setDefaultModel }
}
