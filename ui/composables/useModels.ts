import { LlmProxyServiceRequiredException } from "~/types/Errors"
import type { LlmModelResponse } from "~/types/Schemas"

const models = ref<LlmModelResponse[]>([])
const defaultModel = ref<LlmModelResponse>()
const error = ref<string | null>(null)
const isLoading = ref<boolean>(false)
const loaded = ref<boolean>(false)

export default function useModels() {
   const settings = getSettings()

   const defaultModelConfig = computed(() => settings?.value.llmDefaultModel)

   const llmService = getLlmProxyService()

   const getModels = async () => {
      if (models.value.length <= 0) {
         try {
            if (!llmService.value) throw new LlmProxyServiceRequiredException()
            isLoading.value = true
            const response = await llmService.value.getModels()
            models.value = response.models
            loaded.value = true
         } catch (err) {
            error.value = err instanceof Error ? err.message : String(err)
            loaded.value = false
         } finally {
            isLoading.value = false
         }
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

   return {
      models,
      defaultModel,
      setDefaultModel,
      getModels,
      isLoading,
      loaded,
      error
   }
}
