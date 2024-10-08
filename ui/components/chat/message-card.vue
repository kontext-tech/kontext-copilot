<template>
   <div class="py-1 d-flex align-items-top mx-1">
      <div class="flex-shink-0 chat-icon">
         <Icon
            v-if="message.role !== ChatRoles.SYSTEM"
            :name="getRoleIcon(message.role)"
            size="24"
            :class="getRoleClass(message.role)"
         />
      </div>

      <div
         class="flex-wrap d-flex flex-column"
         :class="{ 'flex-grow-1': hasCharts, 'flex-grow-0': !hasCharts }"
      >
         <div class="px-1 d-flex align-items-center">
            <strong v-if="message.role === ChatRoles.USER">{{
               username
            }}</strong>
            <strong v-else-if="message.role === ChatRoles.ASSISTANT">{{
               getRoleName(message.role)
            }}</strong>
            <BSpinner
               v-if="message.generating"
               variant="success"
               small
               class="ms-1"
            />
         </div>
         <div
            v-dompurify-html="htmlMessage"
            class="p-3 rounded bg-body-tertiary my-1 message-card"
            :class="{ 'bg-danger-subtle': message.isError }"
         />
         <div v-if="message.generating">
            <BButton
               v-if="message.isStreaming"
               v-b-tooltip.click.top
               variant="link"
               size="sm"
               class="text-danger"
               title="Aborted!"
               @click="abort"
            >
               <Icon name="material-symbols:stop-circle-outline" />
            </BButton>
         </div>
         <div v-else class="d-flex gap-1">
            <BButton
               v-if="
                  message.isError !== true && message.role !== ChatRoles.SYSTEM
               "
               v-b-tooltip.click.top
               variant="link"
               size="sm"
               class="text-muted"
               title="Copied!"
               @click="copyMessage"
               ><Icon name="material-symbols:content-copy-outline" />
            </BButton>
            <ChatActionBar
               v-if="
                  message.actions &&
                  message.actions.actions &&
                  message.actions.actions.length > 0
               "
               :actions="message.actions"
               :message-id="message.id"
               @run-sql="runSql"
               @user-input="
                  (userInput: string) => emits('user-input', userInput)
               "
            ></ChatActionBar>

            <BButton
               v-if="message.isError"
               v-b-tooltip.click.top
               variant="link"
               size="sm"
               class="text-danger"
               title="Deleted!"
               @click="deleteMsg"
               ><Icon name="material-symbols:delete-outline" />
            </BButton>
         </div>
         <!--Recommend charts-->
         <div v-if="hasCharts" class="mt-1 col-xxl-8">
            <ChartRecommended
               :data-provider-info="dataProviderInfo"
               :data-source-id="dataSourceId"
               :schema-selector="schemaSelector"
               :message="message"
               @chart-generated="handleChartGenerated"
            />
         </div>
      </div>
   </div>
</template>

<script setup lang="ts">
import type { ChatMessageCardProps } from "~/types/UIProps"
import markdownit from "markdown-it"
import { useClipboard } from "@vueuse/core"
import { ChatRoles, ActionTypes } from "~/types/Schemas"
import tableClassPlugin from "~/utils/MarkdownitTableClass"

const props = defineProps<ChatMessageCardProps>()

const md = new markdownit()
md.use(tableClassPlugin, {
   defaultClass: "table table-hover table-sm text-break",
   parentElement: "div",
   parentElementClass: "table-responsive"
})

const htmlMessage = computed(() => {
   if (props.message.generating && props.message.content === "")
      return "<em>Thinking...</em>"
   return md.render(props.message.content)
})

const { copy } = useClipboard()

const hasCharts = computed(() => {
   return (
      props.message.actions &&
      props.message.actions.actions &&
      props.message.actions.actions.includes(ActionTypes.RECOMMEND_CHARTS)
   )
})

const copyMessage = async () => {
   if (props.message.content) copy(props.message.content)
}

const abort = () => {
   emits("abort-clicked")
}

const deleteMsg = () => {
   emits("delete-clicked", props.message.id)
}

const runSql = (sql: string, messageId?: number) => {
   emits("run-sql-clicked", sql, messageId)
}

const handleChartGenerated = (messageId: number) => {
   emits("chart-generated", messageId)
}
const emits = defineEmits([
   "abort-clicked",
   "delete-clicked",
   "run-sql-clicked",
   "user-input",
   "chart-generated"
])
</script>
