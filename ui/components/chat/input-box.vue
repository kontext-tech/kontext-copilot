<template>
   <div class="flex-shrink-0 d-flex align-items-center mx-1">
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
            v-model="input"
            class="form-control"
            type="text"
            placeholder="Ask a question..."
            :disabled="inputDisabled"
            @keydown.enter.prevent="sendMessage"
         />
         <button
            class="btn btn-primary"
            type="button"
            :disabled="buttonDisabled"
            @click="sendMessage"
         >
            <Icon name="material-symbols:send" size="20" />
         </button>
      </div>
   </div>
</template>
<script setup lang="ts">
import { ChatRoles } from "~/types/Schemas"

const input = defineModel<string>({ required: true })

const emits = defineEmits(["send-message"])

const sendMessage = () => {
   if (input.value) {
      emits("send-message", input.value)
   }
}

const chatInput = ref<HTMLTextAreaElement | null>(null)

defineExpose({ chatInput })

const inputDisabled = computed(() => {
   return props.generating === true
})

const buttonDisabled = computed(() => {
   return input.value?.trim().length === 0 || props.generating === true
})

const props = defineProps<{
   generating?: boolean
}>()
</script>
