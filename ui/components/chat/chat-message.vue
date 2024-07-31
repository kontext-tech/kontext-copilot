<template>
   <div class="py-3 d-flex align-items-top">
      <div class="chat-icon">
         <Icon
            :name="getRoleIcon(message.role)"
            size="24"
            :class="getRoleClass(message.role)"
         />
      </div>

      <div class="flex-grow-1 d-flex flex-column">
         <div class="px-1">
            <strong v-if="message.role === ChatRole.USER">{{
               username
            }}</strong>
            <strong v-else>{{ getRoleName(message.role) }}</strong>
         </div>
         <div class="p-3 rounded bg-body-tertiary my-2" v-html="htmlMessage" />
         <div v-if="!message.generating">
            <span
               v-b-tooltip.click.top
               class="text-muted cursor-pointer"
               title="Copied!"
               @click="copyMessage"
            >
               <Icon name="material-symbols:content-copy-outline" size="18" />
            </span>
         </div>
      </div>
   </div>
</template>

<script setup lang="ts">
import type { ChatMessageProps } from "~/types/UIProps"
import markdownit from "markdown-it"
import { useClipboard } from "@vueuse/core"
import { ChatRole } from "~/types/Schemas"

const props = defineProps<ChatMessageProps>()

const md = new markdownit()

const htmlMessage = computed(() => {
   if (props.message.generating && props.message.message === "")
      return "<em>Thinking...</em>"
   return md.render(props.message.message)
})

const { copy } = useClipboard()

const copyMessage = async () => {
   copy(props.message.message)
}
</script>

<style scoped lang="scss"></style>
