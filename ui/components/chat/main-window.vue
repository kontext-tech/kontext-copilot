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
                  v-if="!message.isSystemPrompt"
                  :message="message"
                  :username="settings.generalUsername"
                  @delete-clicked="handleDeleteClicked"
                  @run-sql-clicked="handlRunSqlClicked"
                  @abort-clicked="handleAbortClicked"
                  @user-input="handleUserInput"
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
            class="py-4"
            @send-message="sendMessage"
         ></ChatInputBox>
      </div>
   </div>
</template>

<script setup lang="ts">
import type { CopilotChatCallback } from "~/services/CopilotClientService"
import type { ChatWindowProps } from "~/types/UIProps"
import ChatInputBox from "~/components/chat/input-box.vue"

const sessionTitle = defineModel<string>()

const chatMain = ref<HTMLElement | null>(null)
const chatInputBox = ref<InstanceType<typeof ChatInputBox> | null>(null)

const input = ref<string>("")

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
   if (!props.llmOptions?.model) return
   if (props.llmOptions?.streaming || props.dataSourceId !== undefined) {
      copilotClient.chatStreaming(input.value, props.llmOptions.model, callback)
   } else {
      copilotClient.chat(input.value, props.llmOptions.model, callback)
   }
   input.value = ""
}

const handleAbortClicked = () => {
   copilotClient.abort()
}

const handleDeleteClicked = (messageId: number) => {
   copilotClient.deleteSessionMessage(messageId)
}

const handlRunSqlClicked = async (sql: string, messageId?: number) => {
   if (!props.dataSourceId) return
   copilotClient.runCopilotSql(
      props.dataSourceId,
      sql,
      props.schema,
      messageId,
      callback
   )
}

const handleUserInput = (input: string) => {
   if (!props.llmOptions?.model) return
   if (props.llmOptions?.streaming || props.dataSourceId !== undefined) {
      copilotClient.chatStreaming(input, props.llmOptions.model, callback)
   } else {
      copilotClient.chat(input, props.llmOptions.model, callback)
   }
}

const props = defineProps<ChatWindowProps>()

const initSession = async () => {
   if (props.llmOptions?.model) {
      let reinit = true
      // If the data source and model are the same  or are all undefined, reinitialize the session
      if (
         (copilotClient.state.session?.dataSourceId === props.dataSourceId &&
            copilotClient.state.session?.model === props.llmOptions.model) ||
         !props.dataSourceId
      ) {
         reinit = false
      }
      await copilotClient.initCopilotSession(
         {
            model: props.llmOptions.model,
            dataSourceId: props.dataSourceId,
            tables: props.tables,
            schemaName: props.schema
         },
         callback,
         reinit
      )
      if (copilotClient.state.session) {
         sessionTitle.value = copilotClient.state.session.title
      }
   }
}

watch(
   [
      () => props.llmOptions?.model,
      () => props.schema,
      () => props.tables,
      () => props.dataProviderInfo?.model?.id
   ],
   async () => {
      await initSession()
   },
   { deep: true }
)

onMounted(async () => {
   await initSession()
})
</script>
