<template>
   <DefaultLayout>
      <template #header-secondary>
         <LlmSettingsToolbar
            id="llmToolbar"
            ref="llmToolbar"
            model-selector
            settings-button
            streaming-toggle
            :streaming-default="true"
         />
      </template>

      <div class="mt-3 d-flex flex-column min-h-0 h-100 overflow-y-hidden">
         <div class="flex-grow-1 d-flex flex-column overflow-y-hidden">
            <div
               v-if="settings"
               ref="chatMain"
               class="flex-grow-1 flex-shrink-1 overflow-y-auto px-4"
            >
               <template
                  v-for="(message, i) in copilotClient.state.messages"
                  :key="`${i}-${message.role}`"
               >
                  <ChatMessageCard
                     v-if="message.isSystemPrompt === undefined"
                     :message="message"
                     :username="settings.generalUsername"
                     @delete-clicked="handleDeleteClicked"
                     @abort-clicked="handleAbortClicked"
                  />
               </template>
               <ChatMessageCard
                  v-if="
                     copilotClient.state.currentMessage &&
                     copilotClient.state.generating
                  "
                  :key="`current-${copilotClient.state.currentMessage.id}`"
                  :message="copilotClient.state.currentMessage"
                  :username="settings.generalUsername"
                  @delete-clicked="handleDeleteClicked"
                  @abort-clicked="handleAbortClicked"
               />
            </div>
            <div class="flex-shrink-0 p-4 d-flex align-items-center mx-1">
               <span class="chat-icon">
                  <Icon
                     :name="getRoleIcon(ChatRoles.USER)"
                     size="24"
                     :class="getRoleClass(ChatRoles.USER)"
                  />
               </span>
               <div class="input-group">
                  <input
                     ref="chatInput"
                     v-model="userInput"
                     class="form-control"
                     type="text"
                     placeholder="Type a message..."
                     :disabled="copilotClient.state.generating"
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
import LlmSettingsToolbar from "~/components/llm/settings-toolbar.vue"
import DefaultLayout from "~/layouts/default-layout.vue"
import type { CopilotChatCallback } from "~/services/CopilotClientService"
import { ChatRoles } from "~/types/Schemas"
import { LlmModelRequiredException } from "~/types/Errors"

const userInput = ref<string>("")
const chatMain = ref<HTMLElement | null>(null)
const chatInput = ref<HTMLTextAreaElement | null>(null)
const llmToolbar = ref<InstanceType<typeof LlmSettingsToolbar> | null>(null)

const settings = getSettings()
const copilotClient = getCopilotClientService()

const sendButtonDisabled = computed(
   () => userInput.value.trim().length === 0 || copilotClient.state.generating
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

const callback: CopilotChatCallback = (
   part: string | null,
   message: string | null,
   done: boolean
) => {
   scrollToBottom()
   if (done) userInput.value = ""
}

const sendMessage = async () => {
   if (!llmToolbar.value?.model) throw new LlmModelRequiredException()
   if (llmToolbar.value.streaming)
      copilotClient.chatStreaming(
         userInput.value,
         llmToolbar.value.model,
         callback
      )
   else {
      copilotClient.chat(userInput.value, llmToolbar.value.model, callback)
   }
   userInput.value = ""
}

watch(
   () => llmToolbar.value?.model,
   () => {
      if (llmToolbar.value?.model)
         copilotClient.initCopilotSession(
            { model: llmToolbar.value.model },
            callback,
            true
         )
   }
)

const handleAbortClicked = () => {
   copilotClient.abort()
}

const handleDeleteClicked = (messageId: number) => {
   copilotClient.deleteSessionMessage(messageId)
}
</script>
