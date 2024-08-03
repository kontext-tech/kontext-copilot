import { Ollama, type ListResponse } from "ollama/browser"

class LlmProxyService {
   endpoint: string
   ollama: Ollama

   constructor(endpoint: string) {
      if (endpoint === undefined)
         throw new Error("LlmService requires an endpoint")
      this.endpoint = endpoint
      this.ollama = new Ollama({ host: this.endpoint })
   }

   async getModels(): Promise<ListResponse> {
      return await this.ollama.list()
   }
}

export default LlmProxyService
