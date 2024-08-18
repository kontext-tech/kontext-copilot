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
            <ChatInputBox
               ref="chatInputBox"
               v-model="input"
               :generating="copilotClient.state.generating"
               class="p-4"
               @send-message="sendMessage"
            ></ChatInputBox>
         </div>
      </div>
   </DefaultLayout>
</template>

<script setup lang="ts">
import LlmSettingsToolbar from "~/components/llm/settings-toolbar.vue"
import DefaultLayout from "~/layouts/default-layout.vue"
import type { CopilotChatCallback } from "~/services/CopilotClientService"
import { LlmModelRequiredException } from "~/types/Errors"
import ChatInputBox from "~/components/chat/input-box.vue"

const chatMain = ref<HTMLElement | null>(null)
const chatInputBox = ref<InstanceType<typeof ChatInputBox> | null>(null)

const input = ref<string>("")

const llmToolbar = ref<InstanceType<typeof LlmSettingsToolbar> | null>(null)

const settings = getSettings()
const copilotClient = getCopilotClientService()

usePageTitle()

const scrollToBottom = async () => {
   // Scroll to the bottom of the chat-main element
   await nextTick()
   if (chatMain.value) {
      chatMain.value.scrollTop = chatMain.value.scrollHeight
   }
   chatInputBox.value?.chatInput?.focus()
}

const callback: CopilotChatCallback = (
   part: string | null,
   message: string | null,
   done: boolean
) => {
   scrollToBottom()
   if (done) input.value = ""
}

const sendMessage = async () => {
   if (!llmToolbar.value?.model) throw new LlmModelRequiredException()
   if (llmToolbar.value.streaming)
      copilotClient.chatStreaming(input.value, llmToolbar.value.model, callback)
   else {
      copilotClient.chat(input.value, llmToolbar.value.model, callback)
   }
   input.value = ""
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
