import type { DataProviderInfoWrapModel, ChatMessage } from "./Schemas"

export interface NavItemProps {
   id: string
   to?: string
   icon: string
   text: string
   children?: NavItemProps[]
}

export interface ChatMessageProps {
   message: ChatMessage
   username: string
}

export interface ChatToDataCommonProps {
   dataProviderInfo: DataProviderInfoWrapModel
   selectedSchema?: string
   selectedTables?: string[]
   selectedModelName?: string
}
