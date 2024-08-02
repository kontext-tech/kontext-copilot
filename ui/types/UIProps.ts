import type { DataProviderInfoWrapModel, IChatMessage } from "./Schemas"

export interface NavItemProps {
   id: string
   to?: string
   icon: string
   text: string
   children?: NavItemProps[]
}

export interface ChatMessageProps {
   message: IChatMessage
   username: string
}

export interface ChatToDataCommonProps {
   dataProviderInfo: DataProviderInfoWrapModel
   selectedSchema?: string
   selectedTables?: string[]
   selectedModelName?: string
}
