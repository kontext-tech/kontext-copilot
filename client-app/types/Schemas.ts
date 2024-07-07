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

export type Settings = {
    llm_default_model: string;
    llm_temperature: number;
    llm_api_key: string | null;
    llm_endpoint: string;
    llm_ollama_endpoint: string;
    general_theme: string;
    general_username: string;
}
