<template>
   <NuxtLayout>
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
            <LlmModelSelector
               v-if="dataSourceSelctor?.selectedDataSource"
               ref="modelSelector"
            />
            <LlmSettingsButton v-if="dataSourceSelctor?.selectedDataSource" />
         </template>
         <template
            v-if="dataSourceSelctor?.selectedDataSource"
            #secondary-sidebar
         >
            <DataSourceDisplay
               :selected-data-source="dataSourceSelctor.selectedDataSource"
            />
            <hr >
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
            nav-class="px-4 w-100 mb-3"
            content-class="flex-grow-1 px-4 w-100 inset-0 min-h-0 overflow-y-hidden d-flex flex-column align-items-stretch"
            tab-class="inset-0 min-h-0 overflow-y-hidden"
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
               <DataProviderChatWindow
                  :data-provider-info="dataProviderInfo"
                  :selected-schema="selectedSchema"
                  :selected-tables="selectedTables"
                  :selected-model-name="selectedModelName"
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
               <DataProviderQueryWindow
                  :data-provider-info="dataProviderInfo"
                  :selected-schema="selectedSchema"
                  :selected-tables="selectedTables"
               />
            </BTab>
         </BTabs>
      </DefaultLayout>
   </NuxtLayout>
</template>

<script setup lang="ts">
import DefaultLayout from "~/layouts/default-layout.vue"
import DataSourceSelector from "~/components/data-source/selector.vue"
import type { DataProviderInfoModel } from "~/types/Schemas"
import { DataProviderService } from "~/services/ApiServices"
import DataProviderSchemaSelector from "~/components/data-provider/schema-selector.vue"

const dataSourceSelctor = ref<InstanceType<typeof DataSourceSelector> | null>(
   null
)
const dataProviderInfo = ref<DataProviderInfoModel | null>(null)
const selectedSchema = ref<string>()
const selectedTables = ref<string[]>([])
const modelSelector = ref()
const selectedModelName = computed(() => modelSelector.value?.selectedModelName)

const appConfig = useAppConfig()
const providerService = new DataProviderService(appConfig.apiBaseUrl)

const handleDataSourceSelected = async (dataSourceId: number) => {
   providerService
      .getDataProviderInfo(dataSourceId)
      .then((data) => {
         dataProviderInfo.value = data
      })
      .catch((err) => {
         console.error(err)
      })
}

const handleSchemaChange = (schema?: string) => {
   selectedSchema.value = schema
}

const handleTablesChange = (tables: string[]) => {
   selectedTables.value = tables
}

const refresh = (dataSourceId: number) => {
   // dataProviderInfo.value = null
   providerService
      .getDataProviderInfo(dataSourceId)
      .then((data) => {
         dataProviderInfo.value = data
      })
      .catch((err) => {
         console.error(err)
      })
}

usePageTitle()
</script>
