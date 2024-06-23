import { useStorage } from '@vueuse/core'
import { Ollama, type ListResponse } from 'ollama/browser'

class OllamaLlmService {
    temperature: number
    endpoint: string
    ollama: Ollama

    constructor() {
        const config = useAppConfig()
        this.temperature = useStorage(config.settingKeys.llmTemperture, 0.5).value
        this.endpoint = useStorage(config.settingKeys.llmEndpoint, 'http://localhost:11434').value
        this.ollama = new Ollama({ host: this.endpoint, })
    }

    async getModels(): Promise<ListResponse> {
        return await this.ollama.list()
    }
}

export default OllamaLlmService