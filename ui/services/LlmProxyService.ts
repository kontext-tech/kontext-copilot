import { Ollama, type ListResponse } from "ollama/browser"
import { LlmEndointRequiredException } from "~/types/Errors"

export default class LlmProxyService {
   endpoint: string
   service: Ollama
   models?: ListResponse

   constructor(endpoint: string) {
      if (endpoint === undefined) throw new LlmEndointRequiredException()
      this.endpoint = endpoint
      this.service = new Ollama({ host: this.endpoint })
   }

   async getModels(): Promise<ListResponse> {
      if (this.models === undefined) this.models = await this.service.list()
      return this.models
   }
}
