<template>
   <DefaultLayout>
      <ChatTypeSelector
         v-if="chatState.chatTypeSelector.chatType === undefined"
         v-model="chatState.chatTypeSelector"
         class="mt-3 px-4"
      />
      <template v-if="chatState.chatTypeSelector.chatType" #header-secondary>
         <LlmSettingsToolbar
            v-if="
               chatState.chatTypeSelector.chatType === ChatTypes.CHAT_TO_DATA &&
               chatState
            "
            v-model="chatState.llmOptions"
            model-selector
            settings-button
         />
         <LlmSettingsToolbar
            v-if="
               chatState.chatTypeSelector.chatType === ChatTypes.GENGERAL_CHAT
            "
            v-model="chatState.llmOptions"
            model-selector
            settings-button
            streaming-toggle
            :streaming-default="true"
         />
         <template
            v-if="
               chatState.chatTypeSelector.chatType === ChatTypes.CHAT_TO_DATA
            "
         >
            <DataSourceSelector
               v-model="chatState.dataSource"
               auto-select
               @data-source-selected="handleDataSourceSelected"
            />
            <DataProviderSchemaSelector
               v-if="chatState.dataProvider.model"
               v-model="chatState.schemaSelector"
               :data-provider-info="chatState.dataProvider"
            ></DataProviderSchemaSelector>
         </template>

         <BButton variant="link" class="ms-auto" @click="handleSelectChatType">
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
         v-model="chatState.sessionTitle"
         :llm-options="chatState.llmOptions"
         class="mt-3 px-4"
      ></ChatMainWindow>
      <BTabs
         v-if="
            chatState.dataProvider.model &&
            chatState.chatTypeSelector.chatType === ChatTypes.CHAT_TO_DATA
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
               v-model="chatState.sessionTitle"
               :data-provider-info="chatState.dataProvider"
               :schema="chatState.schemaSelector.schema"
               :tables="chatState.schemaSelector.tables"
               :data-source-id="chatState.dataSource.model?.id"
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
import DefaultLayout from "~/layouts/default-layout.vue"
import { type ChatStateModel, ChatTypes } from "~/types/Schemas"

usePageTitle()

const chatStateDefault: ChatStateModel = {
   sessionTitle: "Chat",
   sql: "",
   schemaSelector: {
      schema: undefined,
      tables: []
   },
   chatTypeSelector: { chatType: undefined, open: true },
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
      format: ""
   }
}

const chatState = ref<ChatStateModel>(chatStateDefault)

const dataProviderService = getDataProviderService()

const reset = () => {
   // Object.assign(chatState.value, chatStateDefault)
   Object.assign(
      chatState.value.schemaSelector,
      chatStateDefault.schemaSelector
   )
   Object.assign(chatState.value.dataSource, chatStateDefault.dataSource)
   Object.assign(chatState.value.dataProvider, chatStateDefault.dataProvider)
   Object.assign(chatState.value.llmOptions, chatStateDefault.llmOptions)
   Object.assign(
      chatState.value.chatTypeSelector,
      chatStateDefault.chatTypeSelector
   )
}

const handleDataSourceSelected = async (dataSourceId: number) => {
   chatState.value.dataProvider.isLoading = true
   dataProviderService
      .getDataProviderInfo(dataSourceId)
      .then((data) => {
         chatState.value.dataProvider.model = data
         chatState.value.schemaSelector.tables = []
         chatState.value.schemaSelector.schema = undefined
      })
      .catch((err) => {
         console.error(err)
      })
      .finally(() => {
         chatState.value.dataProvider.isLoading = false
      })
}

const handleSelectChatType = () => {
   reset()
   chatState.value.chatTypeSelector.chatType = undefined
   chatState.value.chatTypeSelector.open = true
}

const refresh = (dataSourceId: number) => {
   chatState.value.dataProvider.isLoading = true
   dataProviderService
      .getDataProviderInfo(dataSourceId)
      .then((data) => {
         chatState.value.dataProvider.model = data
      })
      .catch((err) => {
         console.error(err)
      })
      .finally(() => {
         chatState.value.dataProvider.isLoading = false
      })
}
</script>
