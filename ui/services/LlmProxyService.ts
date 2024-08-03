import { Ollama, type ListResponse } from "ollama/browser"
import { LlmEndointRequiredException } from "~/types/Errors"

class LlmProxyService {
   endpoint: string
   service: Ollama

   constructor(endpoint: string) {
      if (endpoint === undefined) throw new LlmEndointRequiredException()
      this.endpoint = endpoint
      this.service = new Ollama({ host: this.endpoint })
   }

   async getModels(): Promise<ListResponse> {
      return await this.service.list()
   }
}

export default LlmProxyService
