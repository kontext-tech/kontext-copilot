<template>
   <BModal
      v-model="model.modalOpen"
      size="lg"
      hide-footer
      no-close-on-backdrop
      no-close-on-esc
      title="Select a chat type"
      class="shadow"
      no-fade
   >
      <div class="card-group my-3">
         <!--Start Chat-To-Data-->
         <div class="card border-0">
            <div class="card-body">
               <h4 class="card-title">
                  <Icon name="material-symbols:database-outline" size="24" />
                  Chat to Data
               </h4>
               <p class="text-muted">
                  Use Chat to Data to ask database-related questions. It allows
                  you to run SQL queries and get results quickly.
               </p>
            </div>
            <div
               class="card-footer bg-transparent border-top-0 d-flex align-items-center"
            >
               <BButton
                  variant="primary"
                  @click="handleClick(ChatTypes.CHAT_TO_DATA)"
               >
                  <Icon name="material-symbols:edit-square-outline" />
                  <span class="ms-1">New chat</span>
               </BButton>
            </div>
         </div>

         <!--Start General-Chat-->
         <div class="card border-0">
            <div class="card-body">
               <h4 class="card-title">
                  <Icon name="material-symbols:chat-outline" size="24" />
                  General Chat
               </h4>
               <p class="text-muted">
                  Use this chat to ask questions to large language models
                  (LLMs).
               </p>
            </div>
            <div
               class="card-footer bg-transparent border-top-0 d-flex align-items-center"
            >
               <BButton
                  variant="primary"
                  @click="handleClick(ChatTypes.GENGERAL_CHAT)"
               >
                  <Icon name="material-symbols:edit-square-outline" />
                  <span class="ms-1">New chat</span>
               </BButton>
            </div>
         </div>
      </div></BModal
   >
</template>

<script setup lang="ts">
import { ChatTypes, type ChatTypeSelectorModel } from "~/types/Schemas"

const model = defineModel<ChatTypeSelectorModel>({
   default: { chatType: undefined, open: true, show: true }
})

const handleClick = (chatType: ChatTypes) => {
   model.value.chatType = chatType
   model.value.modalOpen = false
   model.value.show = false
   emits("chat-type-selected", chatType)
}

const emits = defineEmits(["chat-type-selected"])
</script>
