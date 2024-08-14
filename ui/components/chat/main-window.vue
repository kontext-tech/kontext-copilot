<template>
   <div class="d-flex flex-column h-100 overflow-y-hidden">
      <div class="flex-grow-1 d-flex flex-column overflow-y-hidden vh-100">
         <div
            v-if="settings"
            ref="chatMain"
            class="flex-grow-1 flex-shrink-1 overflow-y-auto"
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
                  @run-sql-clicked="handlRunSqlClicked"
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
</template>

<script setup lang="ts">
import type { CopilotChatCallback } from "~/services/CopilotClientService"
import { ChatRoles } from "~/types/Schemas"
import type { ChatToDataCommonProps } from "~/types/UIProps"

const sessionTitle = defineModel<string>("sessionTitle")

const userInput = ref<string>("")
const chatMain = ref<HTMLElement | null>(null)
const chatInput = ref<HTMLTextAreaElement | null>(null)

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
   if (!props.model) return
   copilotClient.chatStreaming(userInput.value, props.model, callback)
   userInput.value = ""
}

const handleAbortClicked = () => {
   copilotClient.abort()
}

const handleDeleteClicked = (messageId: number) => {
   copilotClient.deleteSessionMessage(messageId)
}

const handlRunSqlClicked = async (sql: string) => {
   if (!props.dataSourceId) return
   copilotClient.runCopilotSql(props.dataSourceId, sql, props.schema, callback)
}

const props = defineProps<ChatToDataCommonProps>()

watch(
   [
      () => props.model,
      () => props.schema,
      () => props.tables,
      () => props.dataProviderInfo.provider?.id
   ],
   async () => {
      if (
         props.model &&
         props.dataProviderInfo.provider &&
         props.dataSourceId
      ) {
         let reinit = true
         // If the data source and model are the same, reinitialize the session
         if (
            copilotClient.state.session?.dataSourceId === props.dataSourceId &&
            copilotClient.state.session?.model === props.model
         ) {
            reinit = false
         }
         await copilotClient.initCopilotSession(
            {
               model: props.model,
               dataSourceId: props.dataSourceId,
               tables: props.tables,
               schemaName: props.schema
            },
            callback,
            reinit
         )
         if (copilotClient.state.session)
            sessionTitle.value = copilotClient.state.session.title
      }
   },
   { deep: true }
)
</script>
