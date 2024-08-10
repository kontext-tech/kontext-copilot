import { LlmProxyServiceRequiredException } from "~/types/Errors"
import type { LlmModelResponse } from "~/types/Schemas"

const models = ref<LlmModelResponse[]>([])
const defaultModel = ref<LlmModelResponse>()

export default function useModels() {
   const settings = getSettings()

   const defaultModelConfig = computed(() => settings?.value.llmDefaultModel)

   const llmService = getLlmProxyService()

   const getModels = async () => {
      if (!llmService.value) throw new LlmProxyServiceRequiredException()

      if (models.value.length <= 0) {
         const response = await llmService.value.getModels()
         models.value = response.models
      }
      const model = models.value.find(
         (model) => model.name === defaultModelConfig.value
      )
      if (model) defaultModel.value = model
      else defaultModel.value = models.value[0]
   }

   const setDefaultModel = (model: LlmModelResponse) => {
      defaultModel.value = model
      if (settings) settings.value.llmDefaultModel = model.name
   }

   onMounted(() => {
      getModels()
   })

   return { models, defaultModel, setDefaultModel, getModels }
}
