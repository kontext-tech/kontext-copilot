<template>
   <BAccordion v-if="schema" free>
      <BAccordionItem
         :key="schemaName"
         visible
         body-class="list-group list-group-flush px-0 py-2"
      >
         <template #title>
            <span class="fw-bold">
               <Icon name="material-symbols:schema-outline" /> {{ schemaName }}
            </span>
         </template>
         <div
            v-for="(t, index) in schema.tables"
            :key="index"
            class="list-group-item d-flex align-items-center gap-1 py-0"
         >
            <span class="flex-grow-1">{{ t }}</span>
            <BDropdown
               variant="link"
               toggle-class="text-decoration-none"
               no-caret
            >
               <template #button-content>
                  <Icon name="material-symbols:more-vert" />
               </template>
               <BDropdownItem @click="showSampleDataModal(t)">
                  <Icon name="material-symbols:data-exploration-outline" />
                  Sample data
               </BDropdownItem>
               <BDropdownItem @click="showSqlModal(t, 'CREATE')">
                  <Icon name="material-symbols:code" /> SQL: CREATE TABLE
               </BDropdownItem>
               <BDropdownItem @click="showSqlModal(t, 'SELECT')">
                  <Icon name="material-symbols:code" /> SQL: SELECT
               </BDropdownItem>
            </BDropdown>
         </div>

         <!--Modal for showing sample data-->
         <BModal
            :id="sampleDataModal.id"
            v-model="sampleDataModal.open"
            :title="sampleDataModal.title"
            :size="sampleDataModal.size"
            ok-only
            ok-title="Close"
            @hide="resetSampleDataModal"
         >
            <BAlert
               v-if="sampleDataModal.error"
               :model-value="sampleDataModal.error != null"
               variant="danger"
            >
               {{ sampleDataModal.error }}
            </BAlert>
            <div v-if="sampleDataModal.isLoading">
               <BSpinner variant="primary" />
            </div>
            <div
               v-if="
                  !sampleDataModal.isLoading &&
                  sampleDataModal.data &&
                  sampleDataModal.data.length > 0
               "
               class="table-responsive"
            >
               <BTable
                  striped
                  hover
                  small
                  :items="sampleDataModal.data"
                  :fields="sampleDataFields"
               />
            </div>
            <BAlert
               variant="warning"
               class="d-flex align-items-center"
               :model-value="
                  !sampleDataModal.isLoading &&
                  sampleDataModal.data &&
                  sampleDataModal.data.length == 0
               "
            >
               <Icon name="material-symbols:warning-outline" class="me-1" />
               <span>No records.</span>
            </BAlert>
         </BModal>

         <BModal
            :id="sqlModal.id"
            v-model="sqlModal.open"
            :size="sqlModal.size"
            :title="sqlModal.title"
            @hide="resetSqlModal"
         >
            <template #footer>
               <BButton
                  v-b-tooltip.click.top
                  variant="primary"
                  title="Copied!"
                  @click="copyToClipboard"
               >
                  <Icon name="material-symbols:content-copy-outline" /> Copy
               </BButton>
               <BButton variant="secondary" @click="sqlModal.open = false">
                  Close
               </BButton>
            </template>
            <BAlert
               v-if="sqlModal.error"
               :model-value="sqlModal.error != null"
               variant="danger"
            >
               {{ sqlModal.error }}
            </BAlert>
            <div v-if="sqlModal.isLoading">
               <BSpinner variant="primary" />
            </div>
            <pre>{{ sqlModal.sql }}</pre>
         </BModal>
      </BAccordionItem>
   </BAccordion>
</template>

<script setup lang="ts">
import type { Size } from "bootstrap-vue-next"
import { DataProviderService } from "~/services/ApiServices"
import type {
   DataProviderInfoModel,
   SchemaTablesModel,
   SqlType
} from "~/types/Schemas"
import { useClipboard } from "@vueuse/core"

const schemaName = computed(() => props.schema?.schema ?? "(empty)")

const sampleDataModal = reactive({
   open: false,
   id: "sample-data-modal",
   title: "",
   isLoading: false,
   error: null as string | null,
   size: "xl" as Size,
   data: [] as object[]
})

const currentTable = ref<string | null>(null)
const appConfig = useAppConfig()
const dataProviderService = new DataProviderService(appConfig.apiBaseUrl)

const sampleDataFields = computed(() => {
   if (sampleDataModal.data.length > 0) {
      return Object.keys(sampleDataModal.data[0]).map((key) => ({
         key,
         label: key,
         sortable: true
      }))
   }
   return []
})

const showSampleDataModal = (table: string) => {
   currentTable.value = table
   /*Load sample data */
   if (props.dataProviderInfo?.id) {
      sampleDataModal.isLoading = true
      sampleDataModal.title = currentTable.value
         ? `Sample data for ${props.schema?.schema ? props.schema.schema + "." : ""}${currentTable.value}`
         : "Sample data"
      sampleDataModal.open = true
      dataProviderService
         .getTableSamples(
            props.dataProviderInfo.id,
            table,
            props.schema?.schema ?? undefined
         )
         .then((data) => {
            sampleDataModal.data = data
            sampleDataModal.isLoading = false
         })
         .catch((err) => {
            sampleDataModal.error =
               err instanceof Error
                  ? err.message
                  : "An unexpected error occurred"
            sampleDataModal.isLoading = false
         })
   }
}

const resetSampleDataModal = () => {
   sampleDataModal.title = ""
   sampleDataModal.data = []
   sampleDataModal.isLoading = false
   sampleDataModal.error = null
}

const sqlModal = reactive({
   open: false,
   id: "sql-modal",
   title: "",
   sql: "",
   isLoading: false,
   error: null as string | null,
   size: "lg" as Size
})

const resetSqlModal = () => {
   sqlModal.title = ""
   sqlModal.sql = ""
   sqlModal.isLoading = false
   sqlModal.error = null
}

const showSqlModal = (table: string, sqlType: SqlType) => {
   if (props.dataProviderInfo?.id) {
      sqlModal.isLoading = true
      const table_full_name = props.schema?.schema
         ? `${props.schema.schema}.${table}`
         : table
      sqlModal.title =
         sqlType == "CREATE"
            ? `CREATE TABLE script for: ${table_full_name}`
            : `SELECT script for: ${table_full_name}`
      sqlModal.open = true
      const func =
         sqlType == "CREATE"
            ? dataProviderService.getTableCreationSQL
            : dataProviderService.getTableSelectSQL
      func(props.dataProviderInfo.id, table, props.schema?.schema ?? undefined)
         .then((data) => {
            sqlModal.sql = data.sql
            sqlModal.isLoading = false
         })
         .catch((err) => {
            sqlModal.sql =
               err instanceof Error
                  ? err.message
                  : "An unexpected error occurred"
            sqlModal.isLoading = false
         })
   }
}

const { copy } = useClipboard()

const copyToClipboard = async () => {
   if (sqlModal.sql) {
      await copy(sqlModal.sql)
   }
}

const props = defineProps<{
   schema: SchemaTablesModel | null
   dataProviderInfo: DataProviderInfoModel | null
}>()
</script>
