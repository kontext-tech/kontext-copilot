import type { ModelResponse } from "ollama"
import OllamaLlmService from "~/services/OllamaLlmService"
import { useStorage } from '@vueuse/core'

export default function useOllamaModels() {
    const models = ref<ModelResponse[]>([])

    const defaultModel = ref<ModelResponse>()

    const config = useAppConfig()
    const defaultModelConfig = useStorage(config.settingKeys.llmDefaultModel, "llama3:instruct")

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
        defaultModelConfig.value = model.name
    }

    return { models, defaultModel, setDefaultModel }
}