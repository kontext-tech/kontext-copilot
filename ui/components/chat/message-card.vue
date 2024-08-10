<template>
   <div class="py-1 d-flex align-items-top mx-1">
      <div class="chat-icon">
         <Icon
            v-if="message.role !== ChatRoles.SYSTEM"
            :name="getRoleIcon(message.role)"
            size="24"
            :class="getRoleClass(message.role)"
         />
      </div>

      <div class="flex-grow-1 d-flex flex-column">
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
            <!-- <span v-if="message.id" class="ms-auto text-muted">
               #{{ message.id }}
            </span> -->
         </div>
         <div
            class="p-3 rounded bg-body-tertiary my-1 message-card"
            :class="{ 'bg-danger-subtle': message.isError }"
            v-html="htmlMessage"
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
         <div v-else>
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
            <template
               v-if="message.sqlStatements && message.sqlStatements.length > 0"
            >
               <BButton
                  v-for="(sql, i) in message.sqlStatements"
                  :key="`sql-${i}`"
                  variant="outline-primary"
                  size="sm"
                  title="Run SQL"
                  @click="runSql(sql, i, message.id)"
                  ><Icon name="material-symbols:play-arrow-outline" />
                  <span v-if="i === 0">Run SQL</span>
                  <span v-else>Run SQL {{ i }}</span>
               </BButton>
            </template>

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
      </div>
   </div>
</template>

<script setup lang="ts">
import type { ChatMessageCardProps } from "~/types/UIProps"
import markdownit from "markdown-it"
import { useClipboard } from "@vueuse/core"
import { ChatRoles } from "~/types/Schemas"
import tableClassPlugin from "~/utils/MarkdownitTableClass"

const props = defineProps<ChatMessageCardProps>()

const md = new markdownit()
md.use(tableClassPlugin, {
   defaultClass: "table table-striped table-hover table-sm",
   parentElement: "div",
   parentElementClass: "table-responsive"
})

const htmlMessage = computed(() => {
   if (props.message.generating && props.message.content === "")
      return "<em>Thinking...</em>"
   return md.render(props.message.content)
})

const { copy } = useClipboard()

const copyMessage = async () => {
   copy(props.message.content)
}

const abort = () => {
   emits("abort-clicked")
}

const deleteMsg = () => {
   emits("delete-clicked", props.message.id)
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
