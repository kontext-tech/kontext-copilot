<template>
   <div class="d-flex flex-column h-100 overflow-y-hidden">
      <div class="flex-grow-1 d-flex flex-column overflow-y-hidden vh-100">
         <div
            v-if="settings"
            ref="chatMain"
            class="flex-grow-1 flex-shrink-1 overflow-y-auto"
         >
            <template
               v-for="(message, i) in state.history"
               :key="`${i}-${message.role}`"
            >
               <ChatMessageCard
                  v-if="message.isSystemPrompt === undefined"
                  :message="message"
                  :username="settings.generalUsername"
                  @delete-clicked="handleDeleteClicked"
                  @run-sql-clicked="handlRunSqlClicked"
               />
            </template>
            <ChatMessageCard
               v-if="state.generating"
               :message="state.currentResponse"
               :username="settings.generalUsername"
               @abort-clicked="handleAbortClicked"
            />
         </div>
         <div class="flex-shrink-0 py-4 d-flex align-items-center mx-1">
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
                  placeholder="Ask a question..."
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
</template>

<script setup lang="ts">
import { type LlmChatCallback } from "~/services/CopilotClientService"
import { ChatRoles } from "~/types/Schemas"
import type { ChatToDataCommonProps } from "~/types/UIProps"

const userInput = ref<string>("")
const chatMain = ref<HTMLElement | null>(null)
const chatInput = ref<HTMLTextAreaElement | null>(null)

const settings = getSettings()
const llmClient = getLlmClientService()
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

const callback: LlmChatCallback = (
   part: string,
   message: string | null,
   done: boolean
) => {
   scrollToBottom()
   if (done) userInput.value = ""
}

const sendMessage = async () => {
   if (!props.model) return
   llmClient.chatStreaming(userInput.value, props.model, callback)
   userInput.value = ""
}

const handleAbortClicked = () => {
   llmClient.abort()
}

const handleDeleteClicked = (messageId: number) => {
   llmClient.deleteMessage(messageId)
}

const handlRunSqlClicked = async (sql: string) => {
   if (!props.dataSourceId) return
   llmClient.runCopilotSql(props.dataSourceId, sql, props.schema, callback)
}

const props = defineProps<ChatToDataCommonProps>()

watch(
   [
      () => props.model,
      () => props.schema,
      () => props.tables,
      () => props.dataProviderInfo.provider?.id
   ],
   () => {
      if (
         props.model &&
         props.dataProviderInfo.provider &&
         props.dataSourceId
      ) {
         let reinit = true
         // If the data source and model are the same, reinitialize the session
         if (
            state.session?.dataSourceId === props.dataSourceId &&
            state.session?.model === props.model
         ) {
            reinit = false
         }
         llmClient.init_session(
            {
               model: props.model,
               dataSourceId: props.dataSourceId,
               tables: props.tables,
               schemaName: props.schema
            },
            callback,
            reinit
         )
      }
   },
   { deep: true }
)
</script>
