import type {
   DataProviderService,
   DataSourceService,
   PromptService
} from "~/services/ApiServices"
import type LlmService from "~/services/LlmService"
import {
   NoInjectionContextFoundException,
   ServiceNotFoundException
} from "~/types/Errors"
import type { Settings } from "~/types/Schemas"

interface ServiceNames {
   SETTINGS: unknown
   SETTING_SERVICE: unknown
   PROMPT_SERVICE: unknown
   DATA_SOURCE_SERVICE: unknown
   DATA_PROVIDER_SERVICE: unknown
   LLM_SERVICE: unknown
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

const getSettings = (): Ref<Settings> => {
   return getService<Ref<Settings>>("SETTINGS")
}

const getLlmService = (): Ref<LlmService | null> => {
   return getService<Ref<LlmService>>("LLM_SERVICE")
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

export {
   type ServiceName,
   getService,
   addService,
   getSettings,
   getLlmService,
   getDataSourceService,
   getDataProviderService,
   getPromptService
}
