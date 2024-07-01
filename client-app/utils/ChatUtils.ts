import type { Message } from "ollama";
import  { ChatRole, type IChatMessage } from "~/types/Models";

export const ollmaMessageToChatMessage = (message: Message): IChatMessage => {
    return {
        message: message.content,
        role: message.role as ChatRole
    };
}

export const getRoleClass = (role: ChatRole) => {
    switch (role) {
        case ChatRole.USER:
            return 'bg-primary text-light'
        case ChatRole.ASSISTANT:
            return 'bg-success'
        default:
            return 'bg-secondary'
    }
}

export const getRoleIcon = (role: ChatRole) => {
    switch (role) {
        case ChatRole.USER:
            return 'material-symbols:person-outline'
        case ChatRole.ASSISTANT:
            return 'material-symbols:neurology-outline'
        default:
            return 'material-symbols:settings-outline'
    }
}

export const getRoleName = (role: ChatRole) => {
    switch (role) {
        case ChatRole.USER:
            return 'User'
        case ChatRole.ASSISTANT:
            return 'AI Assistant'
        default:
            return 'System'
    }
}
