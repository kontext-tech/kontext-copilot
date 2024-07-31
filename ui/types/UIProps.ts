import type { DataProviderInfoModel, IChatMessage } from "./Schemas"

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
   dataProviderInfo?: DataProviderInfoModel
   selectedSchema?: string
   selectedTables?: string[]
   selectedModelName?: string
}
