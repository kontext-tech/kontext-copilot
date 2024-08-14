import type LlmProxyService from "./LlmProxyService"
import type { Message } from "ollama/browser"
import {
   ChatRoles,
   type CopilotSessionMessage,
   type SessionInitRequestModel,
   type CopilotState,
   type SettingsModel,
   type LlmChatMessage
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
      }
   }

   private getLocalMessageId() {
      return this.messageIndex--
   }

   private addMessage(message: CopilotSessionMessage) {
      this.state.messages.push(message)
   }

   createUserMessage(content: string, push?: boolean): CopilotSessionMessage {
      const message = {
         id: this.getLocalMessageId(),
         content,
         role: ChatRoles.USER,
         sessionId: this.state.session?.sessionId
      } as CopilotSessionMessage

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

   private updateMessage(part: string, id?: number, done?: boolean) {
      if (this.state.currentMessage) {
         if (part) this.state.currentMessage.content += part
         if (done) this.state.currentMessage.done = done
         if (id) this.state.currentMessage.id = id
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
            } as Message
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

      /*Create another system message about the tables and schema info */
      const content = `Tables selected: ${tables && tables.length > 0 ? tables.join(", ") : "all"}; schema selected: ${schemaName ?? "default"}`
      this.createSystemMessage(content, false, false, undefined, true)
      if (callback) callback(content, content, true)
   }

   async runCopilotSql(
      dataSourceId: number,
      sql: string,
      schema?: string,
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
               sessionId: this.state.session?.sessionId
            },
            () => {}
         )
         this.startGenerating(true)
         for await (const part of response) {
            this.updateMessage(part.message.content, part.id, part.done)
            if (this.state.abort && !part) {
               response.abort()
               this.state.abort = false
               this.stopGenerating()
               break // Abort the loop
            }

            if (callback)
               callback(
                  part.message.content,
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

   async chat(
      input: string,
      model: string,
      callback?: CopilotChatCallback
   ): Promise<LlmChatMessage> {
      // Create user message
      this.createUserMessage(input, true)
      if (callback) callback("", "", false)

      // Create assistant message
      this.state.currentMessage = this.createAssistantMessage("")

      try {
         let response = await this.llmService.service.chat({
            model: model,
            messages: this.getHistory(),
            stream: false,
            options: this.getLlmOptions()
         })
         this.startGenerating()
         if (typeof response === "string") response = JSON.parse(response)
         this.state.currentMessage.content = response.message.content

         if (callback)
            callback(response.message.content, response.message.content, true)
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
      this.createUserMessage(input, true)
      if (callback) callback("", "", false)

      // Create assistant message
      this.state.currentMessage = this.createAssistantMessage("")

      try {
         const response = await this.llmService.service.chat({
            model: model,
            messages: this.getHistory(),
            stream: true,
            options: this.getLlmOptions()
         })
         this.startGenerating(true)

         for await (const part of response) {
            this.updateMessage(part.message.content, undefined, part.done)

            if (this.state.abort && !part.done) {
               response.abort()
               this.state.abort = false
               this.stopGenerating()
               break
            }
            if (callback)
               callback(
                  part.message.content,
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

   async embeddings(prompt: string, model: string): Promise<string> {
      this.state.generatedContent = ""
      this.startGenerating()
      this.llmService.service
         .embeddings({
            model: model,
            prompt: prompt,
            options: this.getLlmOptions()
         })
         .then((response) => {
            this.state.generatedContent = JSON.stringify(response.embedding)
            this.stopGenerating()
            return this.state.generatedContent
         })
      return this.state.generatedContent
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
         const response = await this.llmService.service.generate({
            model: model,
            prompt: promptText,
            system: systemPrompt,
            format: format,
            stream: true,
            options: this.getLlmOptions()
         })
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
         let res = await this.llmService.service.generate({
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
