import axios from "axios"
import { LlmEndointRequiredException } from "~/types/Errors"
import type {
   SessionInitRequestModel,
   SessionInitResponseModel,
   CopilotSessionMessage,
   RunSqlRequestModel,
   ErrorResponseModel,
   LlmModelListResponse,
   ChatRequestModel,
   EmbeddingsRequestModel,
   EmbeddingsResponseModel,
   GenerateRequestModel,
   GenerateResponseModel,
   AddUserMessageRequestModel
} from "~/types/Schemas"
import { AbortableAsyncIterator } from "~/utils/CommonUtils"

axios.defaults.headers.post["Content-Type"] = "application/json"

export default class LlmProxyService {
   endpoint: string
   models?: LlmModelListResponse
   apiBaseUrl: string

   constructor(endpoint: string, apiBaseUrl: string) {
      if (endpoint === undefined) throw new LlmEndointRequiredException()
      this.endpoint = endpoint
      this.apiBaseUrl = apiBaseUrl
      axios.defaults.baseURL = getBaseUrl(apiBaseUrl)
   }

   async getModels(): Promise<LlmModelListResponse> {
      if (this.models === undefined) {
         /* Request without baseURL */
         const response = await axios.get<LlmModelListResponse>(`/copilot/tags`)
         this.models = response.data
      }
      return this.models
   }

   async initSession(
      request: SessionInitRequestModel
   ): Promise<SessionInitResponseModel> {
      const response = await axios.post<SessionInitResponseModel>(
         "/copilot/init-session",
         request
      )
      return response.data
   }

   async addUserMessage(
      request: AddUserMessageRequestModel
   ): Promise<CopilotSessionMessage> {
      const response = await axios.post<CopilotSessionMessage>(
         "/copilot/add-user-message",
         request
      )
      return response.data
   }

   async embeddings(
      request: EmbeddingsRequestModel
   ): Promise<EmbeddingsResponseModel> {
      const response = await axios.post<EmbeddingsResponseModel>(
         "/copilot/embeddings",
         request
      )
      return response.data
   }

   async generateStreaming(
      request: GenerateRequestModel & {
         stream: true
      },
      doneCallback: () => void
   ): Promise<AbortableAsyncIterator<GenerateResponseModel>> {
      const abortController = new AbortController()

      const response = await fetch(
         `${getBaseUrl(this.apiBaseUrl)}/copilot/generate`,
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

      const itr = parseJSON<GenerateResponseModel | ErrorResponseModel>(
         response.body
      )

      const abortableAsyncIterator = new AbortableAsyncIterator(
         abortController,
         itr,
         doneCallback
      )
      return abortableAsyncIterator
   }

   async generate(
      request: GenerateRequestModel & {
         stream?: false
      }
   ): Promise<GenerateResponseModel> {
      const response = await axios.post<GenerateResponseModel>(
         "/copilot/generate",
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
