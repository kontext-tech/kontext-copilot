<template>
   <DefaultLayout>
      <template #header-secondary>
         <DataSourceSelector
            ref="dataSourceSelctor"
            auto-select
            @data-source-selected="handleDataSourceSelected"
         />
         <DataProviderSchemaSelector
            v-if="dataProviderInfo"
            ref="schemaSelector"
            :data-provider-info="dataProviderInfo"
            @schema-changed="handleSchemaChange"
            @tables-changed="handleTablesChange"
         />
         <LlmSettingsToolbar
            v-if="dataSourceSelctor?.selectedDataSource"
            id="llmToolbar"
            ref="llmToolbar"
            model-selector
            settings-button
         />
      </template>
      <template v-if="dataSourceSelctor?.selectedDataSource" #secondary-sidebar>
         <DataSourceDisplay
            v-if="dataSourceSelctor?.selectedDataSource"
            :selected-data-source="dataSourceSelctor.selectedDataSource"
         />
         <hr />
         <DataProviderDisplay
            :data-provider-info="dataProviderInfo"
            @refresh-clicked="refresh"
         />
      </template>

      <div v-if="!dataProviderInfo" class="px-4 mt-3">
         <BAlert
            variant="secondary"
            :model-value="!dataSourceSelctor?.selectedDataSource"
         >
            Please select a data source to start.
         </BAlert>
      </div>
      <BTabs
         v-else
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
                     >Chat to data</span
                  >
               </span>
            </template>
            <ChatMainWindow
               :data-provider-info="dataProviderInfo"
               :schema="selectedSchema"
               :tables="selectedTables"
               :model="selectedModelName"
               :data-source-id="selectedDataSourceId"
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
               :data-provider-info="dataProviderInfo"
               :selected-schema="selectedSchema"
               :selected-tables="selectedTables"
            />
         </BTab>
      </BTabs>
   </DefaultLayout>
</template>

<script setup lang="ts">
import DefaultLayout from "~/layouts/default-layout.vue"
import DataSourceSelector from "~/components/data-source/selector.vue"
import type { DataProviderInfoWrapModel } from "~/types/Schemas"
import DataProviderSchemaSelector from "~/components/data-provider/schema-selector.vue"
import LlmSettingsToolbar from "~/components/llm/settings-toolbar.vue"

const dataSourceSelctor = ref<InstanceType<typeof DataSourceSelector> | null>(
   null
)
const selectedDataSourceId = computed(
   () => dataSourceSelctor.value?.selectedDataSource?.id
)
const dataProviderInfo = reactive<DataProviderInfoWrapModel>({
   isLoading: false,
   provider: null
})
const selectedSchema = ref<string>()
const selectedTables = ref<string[]>([])
const llmToolbar = ref<InstanceType<typeof LlmSettingsToolbar> | null>(null)
const selectedModelName = computed(() => llmToolbar.value?.model)

const dataProviderService = getDataProviderService()

const handleDataSourceSelected = async (dataSourceId: number) => {
   dataProviderInfo.isLoading = true
   dataProviderService
      .getDataProviderInfo(dataSourceId)
      .then((data) => {
         dataProviderInfo.provider = data
      })
      .catch((err) => {
         console.error(err)
      })
      .finally(() => {
         dataProviderInfo.isLoading = false
      })
}

const handleSchemaChange = (schema?: string) => {
   selectedSchema.value = schema
}

const handleTablesChange = (tables: string[]) => {
   selectedTables.value = tables
}

const refresh = (dataSourceId: number) => {
   dataProviderInfo.isLoading = true
   dataProviderService
      .getDataProviderInfo(dataSourceId)
      .then((data) => {
         dataProviderInfo.provider = data
      })
      .catch((err) => {
         console.error(err)
      })
      .finally(() => {
         dataProviderInfo.isLoading = false
      })
}

usePageTitle()
</script>
