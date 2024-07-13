import type { ModelResponse } from "ollama/browser"
import OllamaLlmService from "~/services/OllamaLlmService"
import type { SettingsWrapper } from "~/types/Schemas"

export default function useModels() {
    const models = ref<ModelResponse[]>([])

    const defaultModel = ref<ModelResponse>()

    const settingsWrapper = inject('settings') as Ref<SettingsWrapper>

    const defaultModelConfig = computed(() => settingsWrapper.value.settings.llm_default_model)
    const loaded = computed(() => settingsWrapper.value.loaded)

    let ollamaService: OllamaLlmService
    const getOllamaService = () => {
        if (!ollamaService)
            ollamaService = new OllamaLlmService(settingsWrapper.value.settings.llm_endpoint)
        return ollamaService
    }


    const getModels = async () => {
        const oService = getOllamaService()
        if (!oService) return
        const response = await oService.getModels()
        models.value = response.models
        const model = models.value.find(model => model.name === defaultModelConfig.value)
        if (model)
            defaultModel.value = model
        else
            defaultModel.value = models.value[0]
    }

    watch(loaded, (loaded) => {
        if (loaded) {
            getModels()
        }
    })

    /* persist default model selection to local storage */
    const setDefaultModel = (model: ModelResponse) => {
        defaultModel.value = model
        settingsWrapper.value.settings.llm_default_model = model.name
    }

    onMounted(() => {
        if (loaded.value) {
            getModels()
        }
    })

    return { models, defaultModel, setDefaultModel }
}
