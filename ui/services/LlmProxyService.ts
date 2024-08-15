import axios from "axios"
import { Ollama } from "ollama/browser"
import { LlmEndointRequiredException } from "~/types/Errors"
import type {
   SessionInitRequestModel,
   SessionInitResponseModel,
   CopilotSessionMessage,
   RunSqlRequestModel,
   ErrorResponseModel,
   LlmModelListResponse,
   ChatRequestModel
} from "~/types/Schemas"
import { AbortableAsyncIterator } from "~/utils/CommonUtils"

axios.defaults.headers.post["Content-Type"] = "application/json"

export default class LlmProxyService {
   endpoint: string
   service: Ollama
   models?: LlmModelListResponse
   apiBaseUrl: string

   constructor(endpoint: string, apiBaseUrl: string) {
      if (endpoint === undefined) throw new LlmEndointRequiredException()
      this.endpoint = endpoint
      this.service = new Ollama({ host: this.endpoint })
      this.apiBaseUrl = apiBaseUrl
      axios.defaults.baseURL = getBaseUrl(apiBaseUrl)
   }

   async getModels(): Promise<LlmModelListResponse> {
      if (this.models === undefined) {
         /* Request without baseURL */
         const response = await axios.get<LlmModelListResponse>(
            `${this.apiBaseUrl}/llms/api/tags`
         )
         this.models = response.data
      }
      return this.models
   }

   async initSession(
      request: SessionInitRequestModel
   ): Promise<SessionInitResponseModel> {
      const response = await axios.post<SessionInitResponseModel>(
         "/copilot/init_session",
         request
      )
      return response.data
   }

   async chatStreaming(
      request: ChatRequestModel,
      doneCallback: () => void
   ): Promise<AbortableAsyncIterator<CopilotSessionMessage>> {
      const abortController = new AbortController()

      const response = await fetch(
         `${getBaseUrl(this.apiBaseUrl)}/copilot/chat`,
         {
            method: "POST",
            headers: {
               "Content-Type": "application/json"
            },
            body: JSON.stringify(request),
            signal: abortController.signal
         }
      )

      if (!response.body) {
         throw new Error("No response body")
      }

      const itr = parseJSON<CopilotSessionMessage | ErrorResponseModel>(
         response.body
      )

      const abortableAsyncIterator = new AbortableAsyncIterator(
         abortController,
         itr,
         doneCallback
      )
      return abortableAsyncIterator
   }

   async chat(request: ChatRequestModel): Promise<CopilotSessionMessage> {
      const response = await axios.post<CopilotSessionMessage>(
         "/copilot/chat",
         request
      )
      return response.data
   }

   async runSql(
      request: RunSqlRequestModel,
      doneCallback: () => void
   ): Promise<AbortableAsyncIterator<CopilotSessionMessage>> {
      const abortController = new AbortController()

      const response = await fetch(
         `${getBaseUrl(this.apiBaseUrl)}/copilot/run-sql`,
         {
            method: "POST",
            headers: {
               "Content-Type": "application/json"
            },
            body: JSON.stringify(request),
            signal: abortController.signal
         }
      )

      if (!response.body) {
         throw new Error("No response body")
      }

      const itr = parseJSON<CopilotSessionMessage | ErrorResponseModel>(
         response.body
      )

      const abortableAsyncIterator = new AbortableAsyncIterator(
         abortController,
         itr,
         doneCallback
      )
      return abortableAsyncIterator
   }
}
