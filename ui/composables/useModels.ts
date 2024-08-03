import type { ModelResponse } from "ollama/browser"

const models = ref<ModelResponse[]>([])
const defaultModel = ref<ModelResponse>()

export default function useModels() {
   const settings = getSettings()

   const defaultModelConfig = computed(() => settings?.value.llm_default_model)

   const llmService = getLlmProxyService()

   const getModels = async () => {
      if (!llmService.value) return
      const response = await llmService.value.getModels()
      models.value = response.models
      const model = models.value.find(
         (model) => model.name === defaultModelConfig.value
      )
      if (model) defaultModel.value = model
      else defaultModel.value = models.value[0]
   }

   const setDefaultModel = (model: ModelResponse) => {
      defaultModel.value = model
      if (settings) settings.value.llm_default_model = model.name
   }

   onMounted(() => {
      const llmService = getLlmProxyService()
      if (llmService) getModels()
   })

   return { models, defaultModel, setDefaultModel, getModels }
}
