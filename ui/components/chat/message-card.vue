<template>
   <div class="py-1 d-flex align-items-top">
      <div class="chat-icon">
         <Icon
            :name="getRoleIcon(message.role)"
            size="24"
            :class="getRoleClass(message.role)"
         />
      </div>

      <div class="flex-grow-1 d-flex flex-column">
         <div class="px-1 d-flex align-items-center">
            <strong v-if="message.role === ChatRole.USER">{{
               username
            }}</strong>
            <strong v-else>{{ getRoleName(message.role) }}</strong>
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
            class="p-3 rounded bg-body-tertiary my-1"
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
               v-if="message.isError !== true"
               v-b-tooltip.click.top
               variant="link"
               size="sm"
               class="text-muted"
               title="Copied!"
               @click="copyMessage"
               ><Icon name="material-symbols:content-copy-outline" />
            </BButton>
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
import { ChatRole } from "~/types/Schemas"

const props = defineProps<ChatMessageCardProps>()

const md = new markdownit()

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

const emits = defineEmits(["abort-clicked", "delete-clicked"])
</script>

<style scoped lang="scss"></style>
