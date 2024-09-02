<template>
   <BModal
      v-model="chatTypeSelector.modalOpen"
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
               <DataSourceSelector v-model="dataSourceSelector" auto-select />
               <br />
               <BAlert
                  variant="warning"
                  :model-value="!dataSourceSelector.model"
               >
                  Please add a data source first.
                  <BLink class="btn btn-outline-secondary" to="/data-sources"
                     ><Icon name="material-symbols:add" /> Add</BLink
                  >
               </BAlert>
            </div>
            <div
               class="card-footer bg-transparent border-top-0 d-flex align-items-center"
            >
               <BButton
                  variant="primary"
                  :disabled="!dataSourceSelector.model"
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
import {
   ChatTypes,
   type ChatTypeSelectorModel,
   type DataSourceWrapModel
} from "~/types/Schemas"

const chatTypeSelector = defineModel<ChatTypeSelectorModel>(
   "chatTypeSelector",
   {
      default: { chatType: undefined, modalOpen: true, show: true }
   }
)

const dataSourceSelector = defineModel<DataSourceWrapModel>(
   "dataSourceSelector",
   {
      default: {
         model: null,
         isLoading: false,
         loaded: false
      }
   }
)

const handleClick = (chatType: ChatTypes) => {
   chatTypeSelector.value.chatType = chatType
   chatTypeSelector.value.modalOpen = false
   chatTypeSelector.value.show = false
   emits("chat-type-selected", chatType)
   if (dataSourceSelector.value.model) {
      emits("data-source-selected", dataSourceSelector.value.model.id)
   }
}

const emits = defineEmits(["chat-type-selected", "data-source-selected"])
</script>
