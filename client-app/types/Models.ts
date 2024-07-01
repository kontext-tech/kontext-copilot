export enum ChatRole {
    USER = 'user',
    ASSISTANT = 'assistant',
    SYSTEM = 'system'
}

export interface IChatMessage {
    message: string;
    role: ChatRole;
    generating?: boolean;
}
