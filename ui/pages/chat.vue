<template>
   <DefaultLayout>
      <template #header-secondary>
         <LlmModelSelector ref="modelSelector" />
         <LlmSettingsButton />
      </template>

      <div class="mt-3 d-flex flex-column min-h-0 h-100 overflow-y-hidden">
         <div class="flex-grow-1 d-flex flex-column overflow-y-hidden">
            <div
               v-if="settings"
               ref="chatMain"
               class="flex-grow-1 flex-shrink-1 overflow-y-auto px-4"
            >
               <template
                  v-for="(message, i) in state.history"
                  :key="`${i}-${message.role}`"
               >
                  <ChatMessageCard
                     :message="message"
                     :username="settings.general_username"
                  />
               </template>
               <ChatMessageCard
                  v-if="state.generating"
                  :message="state.currentResponse"
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
               <div class="input-group">
                  <input
                     ref="chatInput"
                     v-model="userInput"
                     class="form-control"
                     type="text"
                     placeholder="Type a message..."
                     :disabled="state.generating"
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
</template>

<script setup lang="ts">
import ChatMessageCard from "~/components/chat/message-card.vue"
import DefaultLayout from "~/layouts/default-layout.vue"
import LlmClientService, {
   type StreamingCallback
} from "~/services/LlmClientService"
import { ChatRole } from "~/types/Schemas"

const userInput = ref<string>("")
const chatMain = ref<HTMLElement | null>(null)
const chatInput = ref<HTMLTextAreaElement | null>(null)
const modelSelector = ref()

const settings = getSettings()
const llmService = getLlmProxyService()
const llmClient: LlmClientService = new LlmClientService(
   llmService.value,
   settings
)
const state = llmClient.state

const sendButtonDisabled = computed(
   () => userInput.value.trim().length === 0 || state.generating
)

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

const callback: StreamingCallback = (
   part: string,
   message: string | null,
   done: boolean
) => {
   scrollToBottom()
   if (done) userInput.value = ""
}

const sendMessage = async () => {
   llmClient.chatStreaming(
      userInput.value,
      modelSelector.value?.selectedModelName,
      callback
   )
   userInput.value = ""
}
</script>
