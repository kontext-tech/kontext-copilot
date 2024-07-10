import { Ollama, type ListResponse } from 'ollama/browser'

class OllamaLlmService {
    endpoint: string
    ollama: Ollama

    constructor(endpoint: string) {
        this.endpoint = endpoint
        this.ollama = new Ollama({ host: this.endpoint, })
    }

    async getModels(): Promise<ListResponse> {
        return await this.ollama.list()
    }
}

export default OllamaLlmService
