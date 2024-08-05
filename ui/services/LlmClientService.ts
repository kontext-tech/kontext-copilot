import type { Message, Options as OllamaOptions } from "ollama/browser"
import type LlmProxyService from "./LlmProxyService"
import {
   ChatRole,
   type ChatMessage,
   type CopilotSessionRequestModel,
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

const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))

/* A service to handle all chats, generation, etc. */
export default class LlmClientService {
   static readonly DEFAULT_RESPONSE: ChatMessage = {
      content: "",
      role: ChatRole.ASSISTANT,
      generating: false
   }
   llmService: LlmProxyService
   dataProviderService: DataProviderService
   settings: Ref<SettingsModel>
   options: Partial<OllamaOptions> = {}
   state: Reactive<LlmClientState> = reactive({
      generating: false,
      history: [],
      error: null,
      currentResponse: { ...LlmClientService.DEFAULT_RESPONSE },
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

      // Setup options
      this.setOptions()
   }

   private setOptions() {
      this.options = {
         temperature: this.settings.value.llm_temperature,
         top_k: this.settings.value.llm_top_k,
         top_p: this.settings.value.llm_top_p,
         seed: this.settings.value.llm_seed
      }
   }

   addUserMessage(message: string) {
      this.state.history.push({
         content: message,
         role: ChatRole.USER,
         id: this.state.messageIndex++
      })
   }

   addAssistantMessage(message: string, checkSql: boolean = true) {
      const msg = {
         content: message,
         role: ChatRole.ASSISTANT,
         id: this.state.messageIndex++
      } as ChatMessage

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
         role: ChatRole.SYSTEM,
         isError,
         isSystemPrompt,
         id: this.state.messageIndex++
      }
      this.state.history.push(msg)
      return msg
   }

   async runSql(
      dataSourceId: number,
      sql: string,
      schema?: string,
      callback?: LlmChatCallback
   ) {
      this.startGenerating()
      const currentResponse = this.state.currentResponse
      currentResponse.role = ChatRole.ASSISTANT
      const result = await this.dataProviderService.runSql(
         dataSourceId,
         sql,
         schema
      )
      let part = "Sure thing!\n"
      currentResponse.content = part
      callback && callback(part, currentResponse.content, false)
      // Pause for 0.5 second
      await delay(500)

      part = "***SQL:***\n"
      currentResponse.content = part
      callback && callback(part, currentResponse.content, false)

      part = "```sql\n" + sql + "\n```"
      currentResponse.content += part
      callback && callback(part, currentResponse.content, false)

      // Pause for 0.5 second
      await delay(500)

      part = "\n***Result:***\n\n"
      currentResponse.content += part
      callback && callback(part, currentResponse.content, false)

      // Pause for 1 second
      await delay(2000)

      if (!result.success) {
         part = result.message ?? "There is an error when executing the SQL.\n"
         currentResponse.content += part
         callback && callback(part, currentResponse.content, true)
         this.addAssistantMessage(currentResponse.content, false)
         this.state.generating = false
      } else {
         const data = result.data as { [key: string]: object }[]
         if (data.length === 0) {
            part = "0 records returned.\n"
         } else {
            part = this.jsonToMarkdownTable(data)
         }

         currentResponse.content += part
         callback && callback(part, currentResponse.content, true)
         this.addAssistantMessage(currentResponse.content, false)
         this.state.generating = false
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

   private jsonToMarkdownTable(
      jsonArray: { [key: string]: object }[],
      maxRecords: number = 10
   ): string {
      if (jsonArray.length === 0) return ""

      // Extract headers from the first object
      const headers = Object.keys(jsonArray[0])
      const totalRecords = jsonArray.length
      const note =
         totalRecords > maxRecords
            ? `(showing first **${maxRecords}** records of **${totalRecords}**)`
            : ""

      // Create the header row
      const headerRow = `| ${headers.join(" | ")} |`
      const separatorRow = `| ${headers.map(() => "---").join(" | ")} |`

      // Create the data rows
      // Limit the number of records to display
      if (jsonArray.length > maxRecords) {
         jsonArray = jsonArray.slice(0, maxRecords)
      }
      const dataRows = jsonArray.map((obj) => {
         return `| ${headers.map((header) => obj[header]).join(" | ")} |`
      })

      // Combine header, separator, and data rows
      return [note, headerRow, separatorRow, ...dataRows].join("\n")
   }

   private startGenerating() {
      this.resetCurrentResponse()
      this.state.generating = true
      this.state.currentResponse.generating = true
   }

   private resetCurrentResponse() {
      this.state.currentResponse = { ...LlmClientService.DEFAULT_RESPONSE }
   }

   private getHistory() {
      /* Only send system prompt  */
      /* Remap message to only include content and role */
      return this.state.history
         .filter(
            (message) =>
               message.isError !== true &&
               (message.role !== ChatRole.SYSTEM ||
                  message.isSystemPrompt === true)
         )
         .map((message) => {
            return {
               content: message.content,
               role: message.role
            }
         })
   }

   async generateSystemPrompt(
      { model, data_source_id, tables, schema }: CopilotSessionRequestModel,
      callback?: LlmChatCallback
   ) {
      this.startGenerating()
      this.state.generating = true
      /* Construct a request object using params */
      const request: CopilotSessionRequestModel = {
         model,
         data_source_id,
         tables,
         schema
      }
      const response = await this.llmService.getSystemPrompt(request)

      /*Check is system prompt with isSystemPrompt true already exists in history */
      const index = this.state.history.findIndex(
         (message) => message.isSystemPrompt === true
      )
      /* If exists, update the content */
      if (index !== -1) {
         this.state.history[index].content = response.prompt
         const content = `Tables selected: ${tables && tables.length > 0 ? tables.join(", ") : "all"}; schema selected: ${schema ?? "default"}`
         if (callback) callback(content, content, true)
         this.state.generating = false
         /* Add another system message about updated tables */
         this.addSystemMessage(content)
         return response
      } else {
         /* Add system prompt to history */
         this.addSystemMessage(response.prompt, false, true)
         if (callback) callback(response.prompt, response.prompt, true)
         this.state.generating = false
         return response
      }
   }

   async chat(
      input: string,
      model: string,
      callback?: LlmChatCallback
   ): Promise<ChatMessage> {
      this.startGenerating()
      this.addUserMessage(input)
      if (callback) callback("", null, false)

      try {
         let response = await this.llmService.service.chat({
            model: model,
            messages: this.getHistory(),
            stream: false,
            options: this.options
         })
         if (typeof response === "string") response = JSON.parse(response)
         this.state.currentResponse.content = response.message.content
         if (callback)
            callback(response.message.content, response.message.content, true)
         this.state.generating = false
         this.addAssistantMessage(response.message.content)
         return {
            content: this.state.currentResponse.content ?? "",
            role: ChatRole.ASSISTANT
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
         options: this.options
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
            role: ChatRole.ASSISTANT
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
            options: this.options
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
            options: this.options
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
            options: this.options
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
