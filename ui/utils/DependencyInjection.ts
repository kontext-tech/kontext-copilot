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

enum ServiceNames {
   settings = "settings",
   settingService = "settingService",
   promptService = "promptService",
   dataSourceService = "dataSourceService",
   dataProviderService = "dataProviderService",
   llmService = "llmService"
}

type ServiceName = keyof typeof ServiceNames

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
   return getService<Ref<Settings>>("settings")
}

const getLlmService = (): Ref<LlmService | null> => {
   return getService<Ref<LlmService>>("llmService")
}

const getDataSourceService = (): DataSourceService => {
   return getService<DataSourceService>("dataSourceService")
}

const getDataProviderService = (): DataProviderService => {
   return getService<DataProviderService>("dataProviderService")
}

const getPromptService = (): PromptService => {
   return getService<PromptService>("promptService")
}

export {
   type ServiceName,
   ServiceNames,
   getService,
   addService,
   getSettings,
   getLlmService,
   getDataSourceService,
   getDataProviderService,
   getPromptService
}
