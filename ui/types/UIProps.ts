import type {
   CopilotSessionMessage,
   DataProviderInfoWrapModel,
   LlmToolbarOptions,
   SchemaSelectorModel
} from "./Schemas"

export interface NavItemProps {
   id: string
   to?: string
   icon: string
   text: string
   children?: NavItemProps[]
   flat?: boolean
}

export interface ChatMessageCardProps {
   message: CopilotSessionMessage
   username: string
   allowAbort?: boolean
}

export interface ChatWindowProps {
   dataProviderInfo?: DataProviderInfoWrapModel
   schemaSelector?: SchemaSelectorModel
   dataSourceId?: number
   llmOptions: LlmToolbarOptions
}

export interface LlmSettingsToolbarProps {
   modelSelector?: boolean
   streamingToggle?: boolean
   jsonToogle?: boolean
   streamingDefault?: boolean
   jsonDefault?: boolean
}
