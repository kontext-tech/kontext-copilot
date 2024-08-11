import type { Message } from "ollama/browser"
import type LlmProxyService from "./LlmProxyService"
import {
   ChatRoles,
   type LlmChatMessage,
   type SessionInitRequestModel,
   type LlmClientState,
   type SettingsModel
} from "~/types/Schemas"
import {
   DataProviderServiceRequiredException,
   LlmProxyServiceRequiredException
} from "~/types/Errors"
import type { Reactive } from "vue"
import type { DataProviderService } from "./ApiServices"

export type LlmChatCallback = (
   part: string,
   message: string | null,
   done: boolean
) => void

// const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))

/* A service to handle all chats, generation, etc. */
export default class CopilotClientService {
   static readonly DEFAULT_RESPONSE: LlmChatMessage = {
      content: "",
      role: ChatRoles.ASSISTANT,
      generating: false
   }
   llmService: LlmProxyService
   dataProviderService: DataProviderService
   settings: Ref<SettingsModel>
   state: Reactive<LlmClientState> = reactive({
      generating: false,
      history: [],
      error: null,
      currentResponse: { ...CopilotClientService.DEFAULT_RESPONSE },
      abort: false,
      messageIndex: 0
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

   addUserMessage(message: string) {
      this.state.history.push({
         content: message,
         role: ChatRoles.USER,
         id: this.state.messageIndex++
      })
   }

   addAssistantMessage(message: string, checkSql: boolean = true) {
      const msg = {
         content: message,
         role: ChatRoles.ASSISTANT,
         id: this.state.messageIndex++
      } as LlmChatMessage

      /* Extract SQL statements from the message */
      if (checkSql) {
         const sqlStatements = this.extractSqlFromMessage(message)
         if (sqlStatements.length > 0) msg.sqlStatements = sqlStatements
      }
      this.state.history.push(msg)
   }

   addSystemMessage(
      message: string,
      isError?: boolean,
      isSystemPrompt?: boolean
   ) {
      const msg = {
         content: message,
         role: ChatRoles.SYSTEM,
         isError,
         isSystemPrompt,
         id: this.state.messageIndex++
      }
      this.state.history.push(msg)
      return msg
   }

   async runCopilotSql(
      dataSourceId: number,
      sql: string,
      schema?: string,
      callback?: LlmChatCallback
   ) {
      this.startGenerating()
      if (callback) callback("", null, false)

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
         this.state.currentResponse.isStreaming = true
         for await (const part of response) {
            if (this.state.abort && !part.done) {
               response.abort()
               this.state.abort = false
               this.state.generating = false
               this.addAssistantMessage(
                  this.state.currentResponse.content ?? ""
               )
            }
            this.state.currentResponse.content += part.message.content
            if (callback)
               callback(
                  part.message.content,
                  this.state.currentResponse.content,
                  part.done
               )
            if (part.done) {
               this.state.generating = false
               this.addSystemMessage(this.state.currentResponse.content ?? "")
            }
         }
         return {
            content: this.state.currentResponse.content ?? "",
            role: ChatRoles.SYSTEM
         }
      } catch (e) {
         this.state.error = e instanceof Error ? e.message : String(e)
         this.state.generating = false
         this.state.currentResponse.content = ""
         return this.addSystemMessage(this.state.error, true)
      }
   }

   private extractSqlFromMessage(message: string): string[] {
      // Regular expression to match code blocks in Markdown, optionally marked with "sql"
      const codeBlockRegex = /```(?:sql)?\s*([\s\S]*?)\s*```/gi

      let match
      const codeBlocks: string[] = []

      // Find all matches
      while ((match = codeBlockRegex.exec(message)) !== null) {
         // Extract the code from the match
         codeBlocks.push(match[1].trim())
      }

      return codeBlocks
   }

   private startGenerating() {
      this.resetCurrentResponse()
      this.state.generating = true
      this.state.currentResponse.generating = true
   }

   private resetCurrentResponse() {
      this.state.currentResponse = { ...CopilotClientService.DEFAULT_RESPONSE }
   }

   private getHistory() {
      /* Only send system prompt  */
      /* Remap message to only include content and role */
      return this.state.history
         .filter(
            (message) =>
               message.isError !== true &&
               (message.role !== ChatRoles.SYSTEM ||
                  message.isSystemPrompt === true)
         )
         .map((message) => {
            return {
               content: message.content,
               role: message.role
            }
         })
   }

   async initCopilotSession(
      { model, dataSourceId, tables, schemaName }: SessionInitRequestModel,
      callback?: LlmChatCallback,
      reinit: boolean = false
   ) {
      this.startGenerating()
      this.state.generating = true
      /* Construct a request object using params */
      const request: SessionInitRequestModel = {
         model,
         dataSourceId,
         tables,
         schemaName
      }
      if (!reinit) request.sessionId = this.state.session?.sessionId
      else {
         this.state.history = []
      }
      const response = await this.llmService.initSession(request)
      this.state.session = response

      /*Check is system prompt with isSystemPrompt true already exists in history */
      const index = this.state.history.findIndex(
         (message) => message.isSystemPrompt === true
      )
      /* If exists, update the content */
      if (index !== -1) {
         this.state.history[index].content = response.systemPrompt
         const content = `Tables selected: ${tables && tables.length > 0 ? tables.join(", ") : "all"}; schema selected: ${schemaName ?? "default"}`
         if (callback) callback(content, content, true)
         this.state.generating = false
         /* Add another system message about updated tables */
         this.addSystemMessage(content)
         return response
      } else {
         /* Add system prompt to history */
         this.addSystemMessage(response.systemPrompt, false, true)
         if (callback)
            callback(response.systemPrompt, response.systemPrompt, true)
         this.state.generating = false
         return response
      }
   }

   async chat(
      input: string,
      model: string,
      callback?: LlmChatCallback
   ): Promise<LlmChatMessage> {
      this.startGenerating()
      this.addUserMessage(input)
      if (callback) callback("", null, false)

      try {
         let response = await this.llmService.service.chat({
            model: model,
            messages: this.getHistory(),
            stream: false,
            options: this.getLlmOptions()
         })
         if (typeof response === "string") response = JSON.parse(response)
         this.state.currentResponse.content = response.message.content
         if (callback)
            callback(response.message.content, response.message.content, true)
         this.state.generating = false
         this.addAssistantMessage(response.message.content)
         return {
            content: this.state.currentResponse.content ?? "",
            role: ChatRoles.ASSISTANT
         }
      } catch (e) {
         this.state.error = e instanceof Error ? e.message : String(e)
         this.state.generating = false
         this.state.currentResponse.content = ""
         return this.addSystemMessage(this.state.error, true)
      }
   }

   async chatStreaming(
      input: string,
      model: string,
      callback: LlmChatCallback
   ): Promise<Message> {
      this.startGenerating()
      this.addUserMessage(input)
      if (callback) callback("", null, false)

      const response = await this.llmService.service.chat({
         model: model,
         messages: this.getHistory(),
         stream: true,
         options: this.getLlmOptions()
      })

      this.state.currentResponse.isStreaming = true
      try {
         for await (const part of response) {
            if (this.state.abort && !part.done) {
               response.abort()
               this.state.abort = false
               this.state.generating = false
               this.addAssistantMessage(
                  this.state.currentResponse.content ?? ""
               )
            }
            this.state.currentResponse.content += part.message.content
            callback(
               part.message.content,
               this.state.currentResponse.content,
               part.done
            )
            if (part.done) {
               this.state.generating = false
               this.addAssistantMessage(
                  this.state.currentResponse.content ?? ""
               )
            }
         }
         return {
            content: this.state.currentResponse.content ?? "",
            role: ChatRoles.ASSISTANT
         }
      } catch (e) {
         this.state.error = e instanceof Error ? e.message : String(e)
         this.state.generating = false
         this.state.currentResponse.content = ""
         return this.addSystemMessage(this.state.error, true)
      }
   }

   private replaceValues(promt: string, userInput: string) {
      return promt.replace(/\{\{\$input\}\}/g, userInput)
   }

   async generate(
      prompt: string,
      userInput: string,
      model: string,
      format: "json" | "",
      stream: boolean,
      callback?: LlmChatCallback,
      systemPrompt?: string
   ) {
      const promptText =
         prompt !== "" ? this.replaceValues(prompt, userInput) : userInput
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
         this.state.currentResponse.isStreaming = true
         for await (const part of response) {
            if (this.state.abort && !part.done) {
               response.abort()
               this.state.abort = false
               this.state.generating = false
               this.addAssistantMessage(
                  this.state.currentResponse.content ?? ""
               )
            }
            this.state.currentResponse.content += part.response
            if (callback)
               callback(
                  part.response,
                  this.state.currentResponse.content,
                  part.done
               )
            if (part.done) {
               this.state.generating = false
               this.addAssistantMessage(
                  this.state.currentResponse.content ?? ""
               )
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
         this.state.currentResponse.content = res.response
         this.state.generating = false
         this.addAssistantMessage(this.state.currentResponse.content)
      }
   }

   async embeddings(prompt: string, model: string): Promise<string> {
      this.startGenerating()
      this.llmService.service
         .embeddings({
            model: model,
            prompt: prompt,
            options: this.getLlmOptions()
         })
         .then((response) => {
            this.state.currentResponse.content = JSON.stringify(
               response.embedding
            )
         })
         .finally(() => {
            this.state.generating = false
         })
      return this.state.currentResponse.content
   }

   abort() {
      this.state.abort = true
   }

   deleteMessage(messageId: number) {
      const index = this.state.history.findIndex(
         (message) => message.id === messageId
      )
      if (index !== -1) {
         this.state.history.splice(index, 1)
      }
   }
}
