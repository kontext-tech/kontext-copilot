<template>
   <DefaultLayout>
      <ChatTypeSelector
         v-if="chatState.chatTypeSelector.show"
         v-model:chat-type-selector="chatState.chatTypeSelector"
         v-model:data-source-selector="chatState.dataSource"
         class="mt-3 px-4"
         @chat-type-selected="handleChatTypeSelected"
         @data-source-selected="handleDataSourceSelected"
      />
      <template #header-tools>
         <LlmModelSelector simple />
      </template>
      <template v-if="chatState.chatTypeSelector.chatType" #header-secondary>
         <LlmSettingsToolbar
            v-if="
               chatState.chatTypeSelector.chatType === ChatTypes.CHAT_TO_DATA &&
               chatState
            "
            v-model="chatState.llmOptions"
            settings-button
         />
         <LlmSettingsToolbar
            v-if="
               chatState.chatTypeSelector.chatType === ChatTypes.GENGERAL_CHAT
            "
            v-model="chatState.llmOptions"
            settings-button
            streaming-toggle
            :streaming-default="true"
         />
         <template
            v-if="
               chatState.chatTypeSelector.chatType === ChatTypes.CHAT_TO_DATA
            "
         >
            <DataProviderSchemaSelector
               v-if="chatState.dataProvider.model"
               v-model="chatState.schemaSelector"
               :data-provider-info="chatState.dataProvider"
            ></DataProviderSchemaSelector>
         </template>
         <BButton
            variant="link"
            class="d-flex align-items-center gap-1 ms-auto"
            @click="showChatSelector"
         >
            <Icon name="material-symbols:edit-square-outline" />
            New chat
         </BButton>
      </template>
      <template
         v-if="
            chatState.dataProvider.model &&
            chatState.chatTypeSelector.chatType === ChatTypes.CHAT_TO_DATA
         "
         #secondary-sidebar
      >
         <DataSourceDisplay
            v-if="chatState.dataSource"
            :selected-data-source="chatState.dataSource.model"
         />
         <hr />
         <DataProviderDisplay
            :data-provider-info="chatState.dataProvider"
            @refresh-clicked="refresh"
         ></DataProviderDisplay>
      </template>

      <ChatMainWindow
         v-if="chatState.chatTypeSelector.chatType === ChatTypes.GENGERAL_CHAT"
         v-model:session-title="chatState.sessionTitle"
         :llm-options="chatState.llmOptions"
         :chat-type-selector="chatState.chatTypeSelector"
         class="mt-3 px-4"
      ></ChatMainWindow>
      <BTabs
         v-if="
            chatState.chatTypeSelector.chatType === ChatTypes.CHAT_TO_DATA &&
            chatState.dataProvider.model
         "
         class="d-flex flex-column align-items-stretch overflow-y-auto pt-3"
         nav-wrapper-class="flex-grow-0 flex-shrink-0"
         nav-class="px-4 w-auto mb-3"
         content-class="flex-grow-1 px-4 w-auto inset-0 min-h-0 overflow-y-hidden d-flex flex-column align-items-stretch"
         tab-class="w-auto inset-0 min-h-0 overflow-y-hidden"
      >
         <BTab id="chatToDataTab" active>
            <template #title>
               <span class="d-flex align-items-center">
                  <Icon name="material-symbols:chat-outline" /><span
                     class="ms-1"
                     >{{ chatState.sessionTitle }}</span
                  >
               </span>
            </template>
            <ChatMainWindow
               v-if="
                  chatState.chatTypeSelector.chatType ===
                     ChatTypes.CHAT_TO_DATA && chatState.dataProvider.model
               "
               v-model:session-title="chatState.sessionTitle"
               :data-provider-info="chatState.dataProvider"
               :schema-selector="chatState.schemaSelector"
               :data-source-id="chatState.dataSource?.model?.id"
               :llm-options="chatState.llmOptions"
            />
         </BTab>
         <BTab id="queryTab">
            <template #title>
               <span class="d-flex align-items-center">
                  <Icon name="material-symbols:database-outline" /><span
                     class="ms-1"
                     >Query</span
                  >
               </span>
            </template>
            <ChatQueryWindow
               :data-provider-info="chatState.dataProvider"
               :selected-schema="chatState.schemaSelector.schema"
               :selected-tables="chatState.schemaSelector.tables"
            ></ChatQueryWindow>
         </BTab>
      </BTabs>
   </DefaultLayout>
</template>

<script setup lang="ts">
import _ from "lodash"
import DefaultLayout from "~/layouts/default-layout.vue"
import { type ChatStateModel, ChatTypes } from "~/types/Schemas"

usePageTitle()

const chatStateDefault: Readonly<ChatStateModel> = {
   sessionTitle: "Chat",
   sql: "",
   schemaSelector: {
      schema: undefined,
      tables: [],
      selectAll: false
   },
   chatTypeSelector: { chatType: undefined, modalOpen: true, show: true },
   dataSource: {
      model: null,
      isLoading: false,
      loaded: false
   },
   dataProvider: {
      model: null,
      isLoading: false
   },
   llmOptions: {
      streaming: false,
      format: "",
      model: undefined
   }
}

// Create a deep copy of the default state using loadash
const chatState = reactive<ChatStateModel>(_.cloneDeep(chatStateDefault))

const dataProviderService = getDataProviderService()

const reset = () => {
   resetSchemaSelector()
   // Object.assign(chatState.dataSource, _.cloneDeep(chatStateDefault.dataSource))
   Object.assign(
      chatState.dataProvider,
      _.cloneDeep(chatStateDefault.dataProvider)
   )
   // Only reset streaming & format and keep model as is
   chatState.llmOptions.streaming = chatStateDefault.llmOptions.streaming
   chatState.llmOptions.format = chatStateDefault.llmOptions.format
   Object.assign(
      chatState.chatTypeSelector,
      _.cloneDeep(chatStateDefault.chatTypeSelector)
   )
   chatState.sessionTitle = chatStateDefault.sessionTitle
}

const resetSchemaSelector = () => {
   chatState.schemaSelector = _.cloneDeep(chatStateDefault.schemaSelector)
}

const handleDataSourceSelected = async (dataSourceId: number) => {
   chatState.dataProvider.isLoading = true
   await dataProviderService
      .getDataProviderInfo(dataSourceId)
      .then((data) => {
         chatState.dataProvider.model = data
         resetSchemaSelector()
      })
      .catch((err) => {
         console.error(err)
      })
      .finally(() => {
         chatState.dataProvider.isLoading = false
      })
}

const showChatSelector = () => {
   chatState.chatTypeSelector.modalOpen = true
   chatState.chatTypeSelector.show = true
}

const handleChatTypeSelected = (chatType: ChatTypes) => {
   reset()
   chatState.chatTypeSelector.chatType = chatType
   chatState.chatTypeSelector.modalOpen = false
   chatState.chatTypeSelector.show = false
   if (chatState.dataSource.model) {
      handleDataSourceSelected(chatState.dataSource.model.id)
   }
}

const refresh = async (dataSourceId: number) => {
   chatState.dataProvider.isLoading = true
   await dataProviderService
      .getDataProviderInfo(dataSourceId)
      .then((data) => {
         chatState.dataProvider.model = data
      })
      .catch((err) => {
         console.error(err)
      })
      .finally(() => {
         chatState.dataProvider.isLoading = false
      })
}
</script>
