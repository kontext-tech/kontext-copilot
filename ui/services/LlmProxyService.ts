import axios from "axios"
import { Ollama, type ListResponse } from "ollama/browser"
import { LlmEndointRequiredException } from "~/types/Errors"
import type {
   CopilotSessionRequestModel,
   CopilotSessionResponseModel,
   LlmChatResponse,
   CopilotRunSqlRequestModel,
   ErrorResponseModel
} from "~/types/Schemas"
import { AbortableAsyncIterator } from "~/utils/CommonUtils"

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
      this.apiBaseUrl = getBaseUrl(apiBaseUrl)
      axios.defaults.baseURL = this.apiBaseUrl
   }

   async getModels(): Promise<ListResponse> {
      if (this.models === undefined) this.models = await this.service.list()
      return this.models
   }

   async init_session(
      request: CopilotSessionRequestModel
   ): Promise<CopilotSessionResponseModel> {
      const response = await axios.post<CopilotSessionResponseModel>(
         "/copilot/init_session",
         request
      )
      return response.data
   }

   async runSql(
      request: CopilotRunSqlRequestModel,
      doneCallback: () => void
   ): Promise<AbortableAsyncIterator<LlmChatResponse>> {
      const abortController = new AbortController()

      const response = await fetch(`${this.apiBaseUrl}/copilot/run-sql`, {
         method: "POST",
         headers: {
            "Content-Type": "application/json"
         },
         body: JSON.stringify(request),
         signal: abortController.signal
      })

      if (!response.body) {
         throw new Error("No response body")
      }

      const itr = parseJSON<LlmChatResponse | ErrorResponseModel>(response.body)

      const abortableAsyncIterator = new AbortableAsyncIterator(
         abortController,
         itr,
         doneCallback
      )
      return abortableAsyncIterator
   }
}
