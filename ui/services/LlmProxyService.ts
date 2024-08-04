import axios from "axios"
import { Ollama, type ListResponse } from "ollama/browser"
import { LlmEndointRequiredException } from "~/types/Errors"
import type {
   CopilotSessionRequestModel,
   CopilotSessionResponseModel
} from "~/types/Schemas"

axios.defaults.headers.post["Content-Type"] = "application/json"

export default class LlmProxyService {
   endpoint: string
   service: Ollama
   models?: ListResponse
   apiBaseUrl: string

   constructor(endpoint: string, apiBaseUrl: string) {
      if (endpoint === undefined) throw new LlmEndointRequiredException()
      this.endpoint = endpoint
      this.service = new Ollama({ host: this.endpoint })
      this.apiBaseUrl = apiBaseUrl
      axios.defaults.baseURL = getBaseUrl(apiBaseUrl)
   }

   async getModels(): Promise<ListResponse> {
      if (this.models === undefined) this.models = await this.service.list()
      return this.models
   }

   async getSystemPrompt(
      request: CopilotSessionRequestModel
   ): Promise<CopilotSessionResponseModel> {
      const response = await axios.post<CopilotSessionResponseModel>(
         "/copilot/session",
         request
      )
      return response.data
   }
}
