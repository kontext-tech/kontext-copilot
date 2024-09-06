import type {
   ChartTypes,
   ChatTypes,
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
   hidden?: boolean
}

export interface ChatMessageCardProps {
   message: CopilotSessionMessage
   username: string
   allowAbort?: boolean
   dataProviderInfo?: DataProviderInfoWrapModel
   schemaSelector?: SchemaSelectorModel
   dataSourceId?: number
}

export interface ChatWindowProps {
   dataProviderInfo?: DataProviderInfoWrapModel
   schemaSelector?: SchemaSelectorModel
   dataSourceId?: number
   llmOptions: LlmToolbarOptions
   chatType: ChatTypes
}

export interface LlmSettingsToolbarProps {
   modelSelector?: boolean
   streamingToggle?: boolean
   jsonToogle?: boolean
   streamingDefault?: boolean
   jsonDefault?: boolean
}

export interface ChartRecommendedProps {
   message: CopilotSessionMessage
   dataProviderInfo?: DataProviderInfoWrapModel
   schemaSelector?: SchemaSelectorModel
   dataSourceId?: number
}

export interface ChartRendererProps {
   chartData: object
   chartType: ChartTypes
   chartOptions?: object
}
