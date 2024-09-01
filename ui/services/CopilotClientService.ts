import type LlmProxyService from "./LlmProxyService"
import {
   ChatRoles,
   type CopilotSessionMessage,
   type SessionInitRequestModel,
   type CopilotState,
   type SettingsModel,
   type LlmChatMessage,
   type LLmOptions,
   type ActionsModel,
   type ChartDataResponseModel,
   type PieChartModel,
   type BarChartModel,
   type LineChartModel
} from "~/types/Schemas"
import {
   DataProviderServiceRequiredException,
   LlmProxyServiceRequiredException,
   SessionNotFoundException
} from "~/types/Errors"
import type { Reactive } from "vue"
import type { DataProviderService } from "./ApiServices"
import _ from "lodash"

export type CopilotChatCallback = (
   part: string,
   message: string,
   done: boolean
) => void

/* A service to handle all chats, generation, etc. */
export default class CopilotClientService {
   llmService: LlmProxyService
   dataProviderService: DataProviderService
   settings: Ref<SettingsModel>
   messageIndex: number = Number.MAX_SAFE_INTEGER
   state: Reactive<CopilotState> = reactive({
      messages: [],
      abort: false
   })

   constructor(
      llmService: LlmProxyService | null,
      datProviderService: DataProviderService | null,
      settings: Ref<SettingsModel>
   ) {
      if (llmService === null) throw new LlmProxyServiceRequiredException()
      if (datProviderService === null)
         throw new DataProviderServiceRequiredException()
      this.llmService = llmService
      this.dataProviderService = datProviderService
      this.settings = settings
   }

   private getLlmOptions() {
      return {
         temperature: this.settings.value.llmTemperature,
         top_k: this.settings.value.llmTopK,
         top_p: this.settings.value.llmTopP,
         seed: this.settings.value.llmSeed
      } as LLmOptions
   }

   private getLocalMessageId() {
      return this.messageIndex--
   }

   private addMessage(message: CopilotSessionMessage) {
      this.state.messages.push(message)
   }

   async createUserMessage(
      content: string,
      model: string,
      push?: boolean
   ): Promise<CopilotSessionMessage> {
      // Add message to server
      const message = await this.llmService.addUserMessage({
         sessionId: this.state.session?.sessionId,
         content: content,
         model: model
      })

      if (push) this.addMessage(message)
      return message
   }

   createAssistantMessage(
      content: string,
      id?: number,
      push?: boolean
   ): CopilotSessionMessage {
      const message = {
         id: id ?? this.getLocalMessageId(),
         content,
         role: ChatRoles.ASSISTANT,
         sessionId: this.state.session?.sessionId
      } as CopilotSessionMessage
      if (push) this.addMessage(message)
      return message
   }

   createSystemMessage(
      content: string,
      isError?: boolean,
      isSystemPrompt?: boolean,
      id?: number,
      push?: boolean
   ) {
      const message = {
         id: id ?? this.getLocalMessageId(),
         content: content,
         role: ChatRoles.SYSTEM,
         isError,
         isSystemPrompt,
         sessionId: this.state.session?.sessionId
      } as CopilotSessionMessage
      if (push) this.addMessage(message)
      return message
   }

   private startGenerating(isStreaming?: boolean) {
      if (this.state.currentMessage) {
         this.state.currentMessage.generating = true
         if (isStreaming) this.state.currentMessage.isStreaming = isStreaming
      }
      this.state.generating = true
   }

   private stopGenerating() {
      if (this.state.currentMessage)
         this.state.currentMessage.generating = false
      this.state.generating = false
   }

   private updateMessage(
      part: string,
      id?: number,
      done?: boolean,
      actions?: ActionsModel
   ) {
      if (this.state.currentMessage) {
         if (part) this.state.currentMessage.content += part
         if (done) this.state.currentMessage.done = done
         if (id) this.state.currentMessage.id = id
         if (actions) this.state.currentMessage.actions = actions
      }
   }

   private getHistory() {
      /* Only send system prompt, user and assistant messages  */
      /* Remap message to only include content and role */
      return this.state.messages
         .filter(
            (message) =>
               message.isError !== true &&
               (message.role !== ChatRoles.SYSTEM ||
                  message.isSystemPrompt === true)
         )
         .map((message) => {
            return {
               role: message.role,
               content: message.content
            } as LlmChatMessage
         })
   }

   private clearHistory() {
      this.state.messages = []
   }

   private checkSession() {
      if (!this.state.session) {
         throw new SessionNotFoundException()
      }
   }

   async initCopilotSession(
      { model, dataSourceId, tables, schemaName }: SessionInitRequestModel,
      callback?: CopilotChatCallback,
      reinit: boolean = false
   ): Promise<void> {
      /* Construct a request object using params */
      const request: SessionInitRequestModel = {
         model,
         dataSourceId,
         tables,
         schemaName
      }
      if (!reinit) request.sessionId = this.state.session?.sessionId
      else {
         this.clearHistory()
      }

      /*Check is system prompt with isSystemPrompt true already exists in history */
      const index = this.state.messages.findIndex(
         (message) => message.isSystemPrompt === true
      )

      this.state.currentMessage =
         index !== -1
            ? this.state.messages[index]
            : this.createSystemMessage("", false, true)

      this.startGenerating()

      const response = await this.llmService.initSession(request)
      this.state.session = response
      this.state.currentMessage.content = response.systemPrompt
      this.stopGenerating()

      if (callback)
         callback(
            this.state.currentMessage.content,
            this.state.currentMessage.content,
            true
         )
      this.addMessage(this.state.currentMessage)

      if (dataSourceId && !reinit) {
         /*Create another system message about the tables and schema info */
         const content = `Tables selected: ${tables && tables.length > 0 ? tables.join(", ") : "all"}; schema selected: ${schemaName ?? "default"}`
         this.createSystemMessage(content, false, false, undefined, true)
         if (callback) callback(content, content, true)
      }
   }

   async runCopilotSql(
      dataSourceId: number,
      sql: string,
      schema?: string,
      parentMessageId?: number,
      callback?: CopilotChatCallback
   ) {
      this.checkSession()
      if (callback) callback("", "", false)

      this.state.currentMessage = this.createSystemMessage("", false, false)

      try {
         const response = await this.llmService.runSql(
            {
               dataSourceId: dataSourceId,
               sql: sql,
               schemaName: schema,
               sessionId: this.state.session?.sessionId,
               parentMessageId
            },
            () => {}
         )
         this.startGenerating(true)
         for await (const part of response) {
            this.updateMessage(part.content, part.id, part.done, part.actions)
            if (this.state.abort && !part) {
               response.abort()
               this.state.abort = false
               this.stopGenerating()
               break // Abort the loop
            }

            if (callback)
               callback(
                  part.content,
                  this.state.currentMessage.content,
                  part.done ?? false
               )
            if (part.done) {
               this.stopGenerating()
            }
         }
      } catch (e) {
         this.state.currentMessage.content =
            e instanceof Error ? e.message : String(e)
         this.state.currentMessage.isError = true
         this.stopGenerating()
      }
      this.addMessage(this.state.currentMessage)
      return this.state.currentMessage
   }

   async getChartData(
      chart: PieChartModel | BarChartModel | LineChartModel,
      dataSourceId: number,
      schema?: string,
      cached: boolean = true,
      cachedTableName?: string,
      messageId?: number
   ): Promise<ChartDataResponseModel> {
      this.checkSession()
      return await this.llmService.getChartData({
         chart,
         dataSourceId,
         schemaName: schema,
         sessionId: this.state.session?.sessionId,
         cached,
         cachedTableName,
         messageId
      })
   }

   async chat(
      input: string,
      model: string,
      callback?: CopilotChatCallback
   ): Promise<LlmChatMessage> {
      // Create user message
      await this.createUserMessage(input, model, true)
      if (callback) callback("", "", false)

      // Create assistant message
      this.state.currentMessage = this.createAssistantMessage("")

      try {
         this.startGenerating()
         const response = await this.llmService.chat({
            model: model,
            messages: this.getHistory(),
            stream: false,
            format: "",
            options: this.getLlmOptions(),
            sessionId: this.state.session?.sessionId
         })
         this.updateMessage(
            response.content,
            response.id,
            true,
            response.actions
         )

         if (callback) callback(response.content, response.content, true)
      } catch (e) {
         this.state.currentMessage.content =
            e instanceof Error ? e.message : String(e)
         this.state.currentMessage.isError = true
      }
      this.stopGenerating()
      this.addMessage(this.state.currentMessage)
      return this.state.currentMessage
   }

   async chatStreaming(
      input: string,
      model: string,
      callback: CopilotChatCallback
   ): Promise<LlmChatMessage> {
      // Create user message
      await this.createUserMessage(input, model, true)
      if (callback) callback("", "", false)

      // Create assistant message
      this.state.currentMessage = this.createAssistantMessage("")

      try {
         const response = await this.llmService.chatStreaming(
            {
               model: model,
               messages: this.getHistory(),
               stream: true,
               format: "",
               options: this.getLlmOptions(),
               sessionId: this.state.session?.sessionId
            },
            () => {}
         )
         this.startGenerating(true)

         for await (const part of response) {
            this.updateMessage(part.content, part.id, part.done, part.actions)

            if (this.state.abort && !part.done) {
               response.abort()
               this.state.abort = false
               this.stopGenerating()
               break
            }
            if (callback)
               callback(
                  part.content,
                  this.state.currentMessage.content,
                  part.done ?? false
               )
            if (part.done) {
               this.stopGenerating()
            }
         }
      } catch (e) {
         this.state.currentMessage.content =
            e instanceof Error ? e.message : String(e)
         this.state.currentMessage.isError = true
         this.stopGenerating()
      }
      this.addMessage(this.state.currentMessage)
      return this.state.currentMessage
   }

   async embeddings(prompt: string, model: string): Promise<number[]> {
      this.state.generatedEmbeddings = []
      this.startGenerating()
      await this.llmService
         .embeddings({
            model: model,
            prompt: prompt,
            options: this.getLlmOptions()
         })
         .then((response) => {
            this.state.generatedEmbeddings = response.embedding
            this.stopGenerating()
            return this.state.generatedEmbeddings
         })
      return this.state.generatedEmbeddings
   }

   private replaceValues(prompt: string, userInput: string) {
      return prompt.replace(/\{\{\$input\}\}/g, userInput)
   }

   async generate(
      prompt: string,
      userInput: string,
      model: string,
      format: "json" | "",
      stream: boolean,
      callback?: CopilotChatCallback,
      systemPrompt?: string
   ) {
      const promptText =
         prompt !== "" ? this.replaceValues(prompt, userInput) : userInput
      this.state.generatedContent = ""
      this.startGenerating()
      if (stream) {
         const response = await this.llmService.generateStreaming(
            {
               model: model,
               prompt: promptText,
               system: systemPrompt,
               format: format,
               stream: true,
               options: this.getLlmOptions()
            },
            () => {}
         )
         for await (const part of response) {
            this.state.generatedContent += part.response
            if (this.state.abort && !part.done) {
               response.abort()
               this.state.abort = false
               this.stopGenerating()
               break
            }
            if (callback)
               callback(part.response, this.state.generatedContent, part.done)
            if (part.done) {
               this.stopGenerating()
            }
         }
      } else {
         let res = await this.llmService.generate({
            model: model,
            prompt: promptText,
            system: systemPrompt,
            format: format,
            stream: false,
            options: this.getLlmOptions()
         })
         if (typeof res === "string") res = JSON.parse(res)
         this.state.generatedContent = res.response
         this.stopGenerating()
      }
      return this.state.generatedContent
   }

   abort() {
      this.state.abort = true
   }

   deleteSessionMessage(id: number) {
      const index = this.state.messages.findIndex(
         (message) => message.id === id
      )
      if (index !== -1) {
         this.state.messages.splice(index, 1)
      }
   }
}
