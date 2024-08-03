import type { DataProviderInfoWrapModel, ChatMessage } from "./Schemas"

export interface NavItemProps {
   id: string
   to?: string
   icon: string
   text: string
   children?: NavItemProps[]
}

export interface ChatMessageCardProps {
   message: ChatMessage
   username: string
   allowAbort?: boolean
}

export interface ChatToDataCommonProps {
   dataProviderInfo: DataProviderInfoWrapModel
   selectedSchema?: string
   selectedTables?: string[]
   selectedModelName?: string
}

export interface LlmSettingsToolbarProps {
   modelSelector?: boolean
   settingsButton?: boolean
   streamingToggle?: boolean
   jsonToogle?: boolean
   streamingDefault?: boolean
   jsonDefault?: boolean
}
