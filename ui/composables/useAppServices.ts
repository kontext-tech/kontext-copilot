import _ from "lodash"
import {
   DataProviderService,
   DataSourceService,
   PromptService,
   SettingService
} from "~/services/ApiServices"
import type { SettingsModel, SettingsModelWrapper } from "~/types/Schemas"
import LlmProxyService from "~/services/LlmProxyService"
// import type LlmClientService from "~/services/LlmClientService"

const settingsWrapper = reactive<SettingsModelWrapper>({
   isLoading: false,
   loaded: false,
   error: null,
   settings: {} as SettingsModel
})

export default function useAppServices() {
   const appConfig = useAppConfig()

   const settingService = new SettingService(appConfig.apiBaseUrl)
   const promptService = new PromptService(appConfig.apiBaseUrl)
   const dataSourceService = new DataSourceService(appConfig.apiBaseUrl)
   const dataProviderService = new DataProviderService(appConfig.apiBaseUrl)
   const llmProxyService = ref<LlmProxyService | null>(null)
   // const llmClientService = ref<LlmClientService | null>(null)
   const settings = computed(() => settingsWrapper.settings)

   onMounted(() => {
      // Fetch settings on load
      fetchSettings()
   })

   // Function to fetch settings from the API using SettingsService
   const fetchSettings = async () => {
      settingsWrapper.isLoading = true
      try {
         settingsWrapper.settings = await settingService.getSettings()
         const proxy = new LlmProxyService(
            settingsWrapper.settings.llmEndpoint,
            appConfig.apiBaseUrl
         )
         // get models
         // await proxy.getModels()
         llmProxyService.value = proxy
         settingsWrapper.error = null
         settingsWrapper.loaded = true
      } catch (err) {
         settingsWrapper.error =
            err instanceof Error ? err.message : String(err)
      } finally {
         settingsWrapper.isLoading = false
      }
   }

   // Function to update a setting using SettingsService
   const setSetting = async (
      key: keyof SettingsModel,
      value: string | number | null
   ) => {
      try {
         /* Convert key to snake case */
         key = key
            .replace(/([A-Z])/g, "_$1")
            .toLowerCase() as keyof SettingsModel
         await settingService.updateSetting(key, value)
      } catch (err) {
         settingsWrapper.error =
            err instanceof Error ? err.message : String(err)
      }
   }

   watch(
      () => _.cloneDeep(settingsWrapper.settings),
      async (newSettings, oldSettings) => {
         // Determine what changed and call setSetting for those changes
         const keys: Array<keyof SettingsModel> = Object.keys(
            newSettings
         ) as Array<keyof SettingsModel>
         // No need to update to for the initial load
         if (Object.keys(oldSettings).length > 0)
            for (const key of keys) {
               if (oldSettings && newSettings[key] !== oldSettings[key]) {
                  console.log("Updating %s=%s", key, newSettings[key])
                  await setSetting(key, newSettings[key])
               }
            }
      },
      { deep: true }
   )

   // Register global services
   addService("SETTINGS", settings)
   addService("SETTING_SERVICE", settingService)
   addService("PROMPT_SERVICE", promptService)
   addService("DATA_SOURCE_SERVICE", dataSourceService)
   addService("DATA_PROVIDER_SERVICE", dataProviderService)
   addService("LLM_PROXY_SERVICE", llmProxyService)
   // addService("LLM_CLIENT_SERVICE", llmClientService)

   return {
      settingsWrapper
   }
}
