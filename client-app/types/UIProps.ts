import type { IChatMessage } from "./Models"

export interface NavItemProps {
    id: string
    to?: string
    icon: string
    text: string
    children?: NavItemProps[]
}


export interface ChatMessageProps {
    message: IChatMessage
}
