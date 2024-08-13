<template>
   <div class="py-1 d-flex align-items-top mx-1">
      <div class="flex-shink-0 chat-icon">
         <Icon
            v-if="response.message.role !== ChatRoles.SYSTEM"
            :name="getRoleIcon(response.message.role)"
            size="24"
            :class="getRoleClass(response.message.role)"
         />
      </div>

      <div class="flex-grow-0 flex-wrap d-flex flex-column">
         <div class="px-1 d-flex align-items-center">
            <strong v-if="response.message.role === ChatRoles.USER">{{
               username
            }}</strong>
            <strong v-else-if="response.message.role === ChatRoles.ASSISTANT">{{
               getRoleName(response.message.role)
            }}</strong>
            <BSpinner
               v-if="response.generating"
               variant="success"
               small
               class="ms-1"
            />
            <!-- <span v-if="message.id" class="ms-auto text-muted">
               #{{ message.id }}
            </span> -->
         </div>
         <div
            class="p-3 rounded bg-body-tertiary my-1 message-card"
            :class="{ 'bg-danger-subtle': response.isError }"
            v-html="htmlMessage"
         />
         <div v-if="response.generating">
            <BButton
               v-if="response.isStreaming"
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
         <div v-else>
            <BButton
               v-if="
                  response.isError !== true &&
                  response.message.role !== ChatRoles.SYSTEM
               "
               v-b-tooltip.click.top
               variant="link"
               size="sm"
               class="text-muted"
               title="Copied!"
               @click="copyMessage"
               ><Icon name="material-symbols:content-copy-outline" />
            </BButton>
            <template
               v-if="
                  response.sqlStatements && response.sqlStatements.length > 0
               "
            >
               <BButton
                  v-for="(sql, i) in response.sqlStatements"
                  :key="`sql-${i}`"
                  variant="outline-primary"
                  size="sm"
                  title="Run SQL"
                  @click="runSql(sql, i, response.id)"
                  ><Icon name="material-symbols:play-arrow-outline" />
                  <span v-if="i === 0">Run SQL</span>
                  <span v-else>Run SQL {{ i }}</span>
               </BButton>
            </template>

            <BButton
               v-if="response.isError"
               v-b-tooltip.click.top
               variant="link"
               size="sm"
               class="text-danger"
               title="Deleted!"
               @click="deleteMsg"
               ><Icon name="material-symbols:delete-outline" />
            </BButton>
         </div>
      </div>
   </div>
</template>

<script setup lang="ts">
import type { ChatResponseCardProps } from "~/types/UIProps"
import markdownit from "markdown-it"
import { useClipboard } from "@vueuse/core"
import { ChatRoles } from "~/types/Schemas"
import tableClassPlugin from "~/utils/MarkdownitTableClass"

const props = defineProps<ChatResponseCardProps>()

const md = new markdownit()
md.use(tableClassPlugin, {
   defaultClass: "table table-hover table-sm text-break",
   parentElement: "div",
   parentElementClass: "table-responsive"
})

const htmlMessage = computed(() => {
   if (props.response.generating && props.response.message.content === "")
      return "<em>Thinking...</em>"
   return md.render(props.response.message.content)
})

const { copy } = useClipboard()

const copyMessage = async () => {
   copy(props.response.message.content)
}

const abort = () => {
   emits("abort-clicked")
}

const deleteMsg = () => {
   emits("delete-clicked", props.response.id)
}

const runSql = (sql: string, index: number, messageId?: number) => {
   emits("run-sql-clicked", sql, index, messageId)
}

const emits = defineEmits([
   "abort-clicked",
   "delete-clicked",
   "run-sql-clicked"
])
</script>

<style scoped lang="scss"></style>
