<template>
   <div class="d-flex gap-3">
      <!--Start Chat-To-Data-->
      <div class="col-md-6">
         <div class="card">
            <div class="card-body">
               <h4 class="card-title">Chat to Data</h4>
               <p class="text-muted">
                  Use Chat to Data to ask questions related to databases. It
                  enables you to run SQL queries and get results quickly.
               </p>
               <div class="d-flex align-items-center">
                  <BButton
                     variant="primary"
                     @click="
                        () => {
                           model = ChatTypes.CHAT_TO_DATA
                        }
                     "
                  >
                     <Icon name="material-symbols:edit-square-outline" />
                     <span class="ms-1">New chat</span>
                  </BButton>
               </div>
            </div>
         </div>
      </div>

      <!--Start General-Chat-->
      <div class="col-md-6">
         <div class="card">
            <div class="card-body">
               <h4 class="card-title">General Chat</h4>
               <p class="text-muted">
                  Use general chat to ask questions with large language models
                  (LLMs).
               </p>
               <div class="d-flex align-items-center">
                  <BButton
                     variant="primary"
                     @click="
                        () => {
                           model = ChatTypes.GENGERAL_CHAT
                        }
                     "
                  >
                     <Icon name="material-symbols:edit-square-outline" />
                     <span class="ms-1">New chat</span>
                  </BButton>
               </div>
            </div>
         </div>
      </div>
   </div>
</template>

<script setup lang="ts">
import { ChatTypes } from "~/types/Schemas"

const model = defineModel<ChatTypes>()
</script>
