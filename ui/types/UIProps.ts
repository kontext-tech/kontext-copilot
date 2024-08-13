import type { DataProviderInfoWrapModel, LlmChatResponse } from "./Schemas"

export interface NavItemProps {
   id: string
   to?: string
   icon: string
   text: string
   children?: NavItemProps[]
   flat?: boolean
}

export interface ChatResponseCardProps {
   response: LlmChatResponse
   username: string
   allowAbort?: boolean
}

export interface ChatToDataCommonProps {
   dataProviderInfo: DataProviderInfoWrapModel
   schema?: string
   tables?: string[]
   model?: string
   dataSourceId?: number
}

export interface LlmSettingsToolbarProps {
   modelSelector?: boolean
   streamingToggle?: boolean
   jsonToogle?: boolean
   streamingDefault?: boolean
   jsonDefault?: boolean
}

export interface SchemaSelectorModel {
   schema?: string
   tables: string[]
}
