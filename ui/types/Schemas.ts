enum ChatRole {
    USER = 'user',
    ASSISTANT = 'assistant',
    SYSTEM = 'system'
}

interface IChatMessage {
    message: string;
    role: ChatRole;
    generating?: boolean;
}

interface Settings {
    llm_default_model: string;
    llm_temperature: number;
    llm_api_key: string | null;
    llm_endpoint: string;
    llm_ollama_endpoint: string;
    general_theme: string;
    general_username: string;
    llm_top_p: number;
    llm_top_k: number;
    llm_seed: number;
}

interface SettingsWrapper {
    settings: Settings;
    isLoading: boolean;
    loaded: boolean;
    error: any;
}

interface PromptInfo {
    id: string;
    name: string;
}

interface Prompt extends PromptInfo {
    prompt: string;
    system_prompt?: string;
    user_input: string;
}

interface Prompts {
    prompts: Prompt[];
}


export { ChatRole, type IChatMessage, type Settings, type PromptInfo, type Prompt, type Prompts, type SettingsWrapper }
