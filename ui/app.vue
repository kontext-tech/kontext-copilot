<template>
   <NuxtPage v-if="settingsWrapper.loaded" />
   <BSpinner v-else variant="primary" />
</template>

<script setup lang="ts">
import _ from "lodash"
import {
   DataProviderService,
   DataSourceService,
   PromptService,
   SettingService
} from "./services/ApiServices"
import type { Settings, SettingsWrapper } from "./types/Schemas"
import LlmService from "./services/LlmService"

const appConfig = useAppConfig()
const settingsWrapper = reactive<SettingsWrapper>({
   isLoading: false,
   loaded: false,
   error: null,
   settings: {} as Settings
})
const settingService = new SettingService(appConfig.apiBaseUrl)
const promptService = new PromptService(appConfig.apiBaseUrl)
const dataSourceService = new DataSourceService(appConfig.apiBaseUrl)
const dataProviderService = new DataProviderService(appConfig.apiBaseUrl)
const llmService = ref<LlmService | null>(null)
const settings = computed(() => settingsWrapper.settings)

// Function to fetch settings from the API using SettingsService
const fetchSettings = async () => {
   settingsWrapper.isLoading = true
   try {
      settingsWrapper.settings = await settingService.getSettings()
      llmService.value = new LlmService(settingsWrapper.settings.llm_endpoint)
      settingsWrapper.error = null
      settingsWrapper.loaded = true
   } catch (err) {
      settingsWrapper.error = err instanceof Error ? err.message : String(err)
   } finally {
      settingsWrapper.isLoading = false
   }
}

// Function to update a setting using SettingsService
const setSetting = async (key: string, value: string | number | null) => {
   try {
      await settingService.updateSetting(key, value)
   } catch (err) {
      settingsWrapper.error = err instanceof Error ? err.message : String(err)
   }
}

watch(
   () => _.cloneDeep(settingsWrapper.settings),
   async (newSettings, oldSettings) => {
      // Determine what changed and call setSetting for those changes
      const keys: Array<keyof Settings> = Object.keys(newSettings) as Array<
         keyof Settings
      >
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

// Fetch settings on load
fetchSettings()
addService(ServiceNames.settings, settings)
addService(ServiceNames.settingService, settingService)
addService(ServiceNames.promptService, promptService)
addService(ServiceNames.dataSourceService, dataSourceService)
addService(ServiceNames.dataProviderService, dataProviderService)
addService(ServiceNames.llmService, llmService)
</script>

<style scoped></style>
