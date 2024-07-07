import type { ModelResponse } from "ollama/browser"
import OllamaLlmService from "~/services/OllamaLlmService"

export default function useOllamaModels() {
    const models = ref<ModelResponse[]>([])

    const defaultModel = ref<ModelResponse>()

    const { settings } = useSettings()
    const defaultModelConfig = computed(() => settings.value.llm_default_model)

    onMounted(async () => {
        const service = new OllamaLlmService()
        const response = await service.getModels()
        models.value = response.models
        const model = models.value.find(model => model.name === defaultModelConfig.value)
        if (model)
            defaultModel.value = model
        else
            defaultModel.value = models.value[0]
    })

    /* persist default model selection to local storage */
    const setDefaultModel = (model: ModelResponse) => {
        defaultModel.value = model
        settings.value.llm_default_model = model.name
    }

    return { models, defaultModel, setDefaultModel }
}
