import type {
   DataProviderService,
   DataSourceService,
   PromptService
} from "~/services/ApiServices"
import LlmClientService from "~/services/LlmClientService"
import type LlmProxyService from "~/services/LlmProxyService"
import {
   NoInjectionContextFoundException,
   ServiceNotFoundException
} from "~/types/Errors"
import type { SettingsModel } from "~/types/Schemas"

interface ServiceNames {
   SETTINGS: unknown
   SETTING_SERVICE: unknown
   PROMPT_SERVICE: unknown
   DATA_SOURCE_SERVICE: unknown
   DATA_PROVIDER_SERVICE: unknown
   LLM_PROXY_SERVICE: unknown
   LLM_CLIENT_SERVICE: unknown
}

type ServiceName = keyof ServiceNames

const addService = <T>(name: ServiceName, service: T) => {
   if (hasInjectionContext()) {
      provide(name, service)
   } else throw new NoInjectionContextFoundException()
}

const getService = <T>(name: ServiceName): T => {
   if (hasInjectionContext()) {
      const service = inject(name) as T
      if (service === undefined) throw new ServiceNotFoundException(name)
      return service
   } else throw new NoInjectionContextFoundException()
}

const getSettings = (): Ref<SettingsModel> => {
   return getService<Ref<SettingsModel>>("SETTINGS")
}

const getLlmProxyService = (): Ref<LlmProxyService | null> => {
   return getService<Ref<LlmProxyService | null>>("LLM_PROXY_SERVICE")
}

const getDataSourceService = (): DataSourceService => {
   return getService<DataSourceService>("DATA_SOURCE_SERVICE")
}

const getDataProviderService = (): DataProviderService => {
   return getService<DataProviderService>("DATA_PROVIDER_SERVICE")
}

const getPromptService = (): PromptService => {
   return getService<PromptService>("PROMPT_SERVICE")
}

const getLlmClientService = (): LlmClientService => {
   const settings = getSettings()
   const llmProxyService = getLlmProxyService()
   const dataProviderService = getDataProviderService()
   return new LlmClientService(
      llmProxyService.value,
      dataProviderService,
      settings
   )
}

export {
   type ServiceName,
   getService,
   addService,
   getSettings,
   getLlmProxyService,
   getLlmClientService,
   getDataSourceService,
   getDataProviderService,
   getPromptService
}
