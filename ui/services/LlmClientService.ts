import type { Message, Options as OllamaOptions } from "ollama/browser"
import type LlmProxyService from "./LlmProxyService"
import {
   ChatRole,
   type ChatMessage,
   type LlmClientState,
   type Settings
} from "~/types/Schemas"
import { LlmProxyServiceRequiredException } from "~/types/Errors"
import type { Reactive } from "vue"

export type LlmChatCallback = (
   part: string,
   message: string | null,
   done: boolean
) => void

/* A service to handle all chats, generation, etc. */
export default class LlmClientService {
   static readonly DEFAULT_RESPONSE: ChatMessage = {
      content: "",
      role: ChatRole.ASSISTANT,
      generating: false
   }
   llmService: LlmProxyService
   settings: Ref<Settings>
   options: Partial<OllamaOptions> = {}
   state: Reactive<LlmClientState> = reactive({
      generating: false,
      history: [],
      error: null,
      currentResponse: { ...LlmClientService.DEFAULT_RESPONSE },
      abort: false
   })

   constructor(llmService: LlmProxyService | null, settings: Ref<Settings>) {
      if (llmService === null) throw new LlmProxyServiceRequiredException()
      this.llmService = llmService
      this.settings = settings

      // Setup options
      this._setOptions()
   }

   _setOptions() {
      this.options = {
         temperature: this.settings.value.llm_temperature,
         top_k: this.settings.value.llm_top_k,
         top_p: this.settings.value.llm_top_p,
         seed: this.settings.value.llm_seed
      }
   }

   addUserMessage(message: string) {
      this.state.history.push({ content: message, role: ChatRole.USER })
   }

   addAssistantMessage(message: string) {
      this.state.history.push({ content: message, role: ChatRole.ASSISTANT })
   }

   startGenerating() {
      this.resetCurrentResponse()
      this.state.generating = true
      this.state.currentResponse.generating = true
   }

   resetCurrentResponse() {
      this.state.currentResponse = { ...LlmClientService.DEFAULT_RESPONSE }
   }

   async chat(
      input: string,
      model: string,
      callback?: LlmChatCallback
   ): Promise<Message> {
      this.startGenerating()
      this.addUserMessage(input)
      if (callback) callback("", null, false)
      let response = await this.llmService.service.chat({
         model: model,
         messages: this.state.history,
         stream: false,
         options: this.options
      })
      if (typeof response === "string") response = JSON.parse(response)
      this.state.currentResponse.content = response.message.content
      if (callback)
         callback(response.message.content, response.message.content, true)
      this.state.generating = false
      this.addAssistantMessage(response.message.content)
      return response.message
   }

   async chatStreaming(
      input: string,
      model: string,
      callback: LlmChatCallback
   ): Promise<Message> {
      this.startGenerating()
      this.addUserMessage(input)
      const response = await this.llmService.service.chat({
         model: model,
         messages: this.state.history,
         stream: true,
         options: this.options
      })

      this.state.currentResponse.isStreaming = true

      for await (const part of response) {
         if (this.state.abort && !part.done) {
            response.abort()
            this.state.abort = false
            this.state.generating = false
            this.addAssistantMessage(this.state.currentResponse.content ?? "")
         }
         this.state.currentResponse.content += part.message.content
         callback(
            part.message.content,
            this.state.currentResponse.content,
            part.done
         )
         if (part.done) {
            this.state.generating = false
            this.addAssistantMessage(this.state.currentResponse.content ?? "")
         }
      }
      return {
         content: this.state.currentResponse.content ?? "",
         role: ChatRole.ASSISTANT
      }
   }

   replaceValues(promt: string, userInput: string) {
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
}
