<template>
   <NuxtLayout>
      <DefaultLayout>
         <template #header-secondary>
            <LlmModelSelector ref="modelSelector" />
            <LlmSettingsButton />
         </template>

         <div class="mt-3 d-flex flex-column min-h-0 h-100 overflow-y-hidden">
            <div class="flex-grow-1 d-flex flex-column overflow-y-hidden">
               <div
                  ref="chatMain"
                  class="flex-grow-1 flex-shrink-1 overflow-y-auto px-4"
               >
                  <template
                     v-for="(message, i) in chatHistory"
                     :key="`${i}-${message.role}`"
                  >
                     <ChatMessage
                        :message="ollmaMessageToChatMessage(message)"
                        :username="settings.general_username"
                     />
                  </template>
                  <ChatMessage
                     v-if="generating"
                     :message="currentResponse"
                     :username="settings.general_username"
                  />
               </div>
               <div class="flex-shrink-0 p-4 d-flex align-items-center">
                  <span class="chat-icon">
                     <Icon
                        :name="getRoleIcon(ChatRole.USER)"
                        size="24"
                        :class="getRoleClass(ChatRole.USER)"
                     />
                  </span>
                  <div v-if="settingsWrapper.loaded" class="input-group">
                     <input
                        ref="chatInput"
                        v-model="userInput"
                        class="form-control"
                        type="text"
                        placeholder="Type a message..."
                        :disabled="generating"
                        @keydown.enter.prevent="sendMessage"
                     />
                     <button
                        class="btn btn-primary"
                        type="button"
                        :disabled="sendButtonDisabled"
                        @click="sendMessage"
                     >
                        <Icon name="material-symbols:send" size="20" />
                     </button>
                  </div>
               </div>
            </div>
         </div>
      </DefaultLayout>
   </NuxtLayout>
</template>

<script setup lang="ts">
import { type Message } from "ollama/browser"
import ChatMessage from "~/components/chat/chat-message.vue"
import DefaultLayout from "~/layouts/default-layout.vue"
import OllamaLlmService from "~/services/OllamaLlmService"
import {
   ChatRole,
   type IChatMessage,
   type SettingsWrapper
} from "~/types/Schemas"

const settingsWrapper = inject("settings") as Ref<SettingsWrapper>
const settings = computed(() => settingsWrapper.value.settings)
const loaded = computed(() => settingsWrapper.value.loaded)

const userInput = ref<string>("")

const sendButtonDisabled = computed(
   () => userInput.value.trim().length === 0 || generating.value
)

const generating = ref(false)

const chatHistory = ref<Message[]>([])

const currentResponse = ref<IChatMessage>({
   role: ChatRole.ASSISTANT,
   message: "",
   generating: false
})

const chatMain = ref<HTMLElement | null>(null)

const chatInput = ref<HTMLTextAreaElement | null>(null)

const modelSelector = ref()

let ollamaService: OllamaLlmService
const getOllamaService = () => {
   if (!ollamaService && loaded.value) {
      ollamaService = new OllamaLlmService(
         settingsWrapper.value.settings.llm_endpoint
      )
   }
   return ollamaService
}

usePageTitle()

const scrollToBottom = async () => {
   // Scroll to the bottom of the chat-main element
   await nextTick()
   if (chatMain.value) {
      chatMain.value.scrollTop = chatMain.value.scrollHeight
   }
   if (chatInput.value) {
      chatInput.value.focus()
   }
}

/* Send user input and getting response */
const sendMessage = async () => {
   generating.value = true
   chatHistory.value.push({ role: "user", content: userInput.value })
   userInput.value = ""
   await scrollToBottom()
   currentResponse.value.generating = true
   const oService = getOllamaService()
   const response = await oService.ollama.chat({
      model: modelSelector.value?.selectedModelName,
      messages: chatHistory.value,
      stream: true,
      options: {
         temperature: settings.value.llm_temperature,
         top_p: settings.value.llm_top_p,
         top_k: settings.value.llm_top_k,
         seed: settings.value.llm_seed
      }
   })
   for await (const part of response) {
      currentResponse.value.message += part.message.content
      await scrollToBottom()
      if (part.done) {
         chatHistory.value.push({
            role: "assistant",
            content: currentResponse.value.message || ""
         })
         generating.value = false
         /* Reset the value */
         currentResponse.value.message = ""
         await scrollToBottom()
      }
   }
}
</script>

<style scoped lang="scss"></style>
