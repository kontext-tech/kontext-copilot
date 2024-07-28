<template>
    <BAccordion v-if="schema" free>
        <BAccordionItem :key="schemaName" visible body-class="list-group list-group-flush px-0 py-2">
            <template #title>
                <span class="fw-bold">
                    <Icon name="material-symbols:schema-outline"></Icon> {{ schemaName }}
                </span>
            </template>
            <div v-for="(t, index) in schema.tables" :key="index"
                class="list-group-item d-flex align-items-center gap-1 py-0">
                <span class="flex-grow-1">{{ t }}</span>
                <BDropdown variant="link" toggle-class="text-decoration-none" noCaret>
                    <template #button-content>
                        <Icon name="material-symbols:more-vert"></Icon>
                    </template>
                    <BDropdownItem @click="showSampleDataModal(t)">
                        <Icon name="material-symbols:data-exploration-outline"></Icon> Sample data
                    </BDropdownItem>
                    <BDropdownItem @click="showSqlModal(t, 'CREATE')">
                        <Icon name="material-symbols:code"></Icon> SQL: CREATE TABLE
                    </BDropdownItem>
                    <BDropdownItem @click="showSqlModal(t, 'SELECT')">
                        <Icon name="material-symbols:code"></Icon> SQL: SELECT
                    </BDropdownItem>
                </BDropdown>
            </div>

            <!--Modal for showing sample data-->
            <BModal v-model="sampleDataModal.open" :id="sampleDataModal.id" :title="sampleDataModal.title"
                :size="sampleDataModal.size" okOnly okTitle="Close" @hide="resetSampleDataModal">
                <BAlert v-if="sampleDataModal.error" :model-value="sampleDataModal.error != null" variant="danger">
                    {{ sampleDataModal.error }}
                </BAlert>
                <div v-if="sampleDataModal.isLoading">
                    <BSpinner variant="primary" />
                </div>
                <div v-if="!sampleDataModal.isLoading && sampleDataModal.data && sampleDataModal.data.length > 0"
                    class="table-responsive">
                    <BTable striped hover small :items="sampleDataModal.data" :fields="sampleDataFields" />
                </div>
            </BModal>

            <BModal :id="sqlModal.id" :size="sqlModal.size" v-model="sqlModal.open" :title="sqlModal.title"
                @hide="resetSqlModal">
                <template #footer>
                    <BButton variant="primary" @click="copyToClipboard" v-b-tooltip.click.top title="Copied!">
                        <Icon name="material-symbols:content-copy-outline"></Icon> Copy
                    </BButton>
                    <BButton variant="secondary" @click="sqlModal.open = false">Close
                    </BButton>
                </template>
                <BAlert v-if="sqlModal.error" :model-value="sqlModal.error != null" variant="danger">
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
import type { Size } from 'bootstrap-vue-next'
import { DataProviderService } from '~/services/ApiServices'
import type { DataProviderInfoModel, SchemaTablesModel, SqlType } from '~/types/Schemas'
import { useClipboard } from '@vueuse/core'

const schemaName = computed(() => schema?.schema ?? "(empty)")

const sampleDataModal = reactive({
    open: false,
    id: 'sample-data-modal',
    title: '',
    isLoading: false,
    error: null as string | null,
    size: 'xl' as Size,
    data: [] as object[]
})

const currentTable = ref<string | null>(null)
const appConfig = useAppConfig()
const dataProviderService = new DataProviderService(appConfig.apiBaseUrl)

const sampleDataFields = computed(() => {
    if (sampleDataModal.data.length > 0) {
        return Object.keys(sampleDataModal.data[0]).map((key) => ({ key, label: key, sortable: true }));
    }
    return [];
});

const showSampleDataModal = (table: string) => {
    currentTable.value = table
    /*Load sample data */
    if (dataProviderInfo?.id) {
        sampleDataModal.isLoading = true
        dataProviderService.getTableSamples(dataProviderInfo.id, table, schema?.schema ?? undefined).then((data) => {
            sampleDataModal.data = data
            sampleDataModal.title = currentTable.value ? `Sample data for ${schema?.schema ? schema.schema + '.' : ''}${currentTable.value}` : "Sample data"
            sampleDataModal.open = true
            sampleDataModal.isLoading = false
        }).catch((err) => {
            sampleDataModal.error = err instanceof Error ? err.message : 'An unexpected error occurred';
            console.error(sampleDataModal.error)
            sampleDataModal.open = true
            sampleDataModal.isLoading = false
        })
    }
}

const resetSampleDataModal = () => {
    sampleDataModal.title = ''
    sampleDataModal.data = []
    sampleDataModal.isLoading = false
    sampleDataModal.error = null
}

const sqlModal = reactive({
    open: false,
    id: 'sql-modal',
    title: '',
    sql: '',
    isLoading: false,
    error: null as string | null,
    size: 'lg' as Size,
})

const resetSqlModal = () => {
    sqlModal.title = ''
    sqlModal.sql = ''
    sqlModal.isLoading = false
    sqlModal.error = null
}

const showSqlModal = (table: string, sqlType: SqlType) => {
    if (dataProviderInfo?.id) {
        sqlModal.isLoading = true
        const func = sqlType == 'CREATE' ? dataProviderService.getTableCreationSQL : dataProviderService.getTableSelectSQL
        func(dataProviderInfo.id, table, schema?.schema ?? undefined).then((data) => {
            let table_full_name = schema?.schema ? `${schema.schema}.${table}` : table
            sqlModal.title = sqlType == 'CREATE' ? `CREATE TABLE script for: ${table_full_name}` :
                `SELECT script for: ${table_full_name}`
            sqlModal.sql = data.sql
            sqlModal.open = true
            sqlModal.isLoading = false
        }).catch((err) => {
            sqlModal.title = 'Error'
            sqlModal.sql = err instanceof Error ? err.message : 'An unexpected error occurred';
            sqlModal.open = true
            sqlModal.isLoading = false
        })
    }
}

const { copy } = useClipboard()

const copyToClipboard = async () => {
    if (sqlModal.sql) {
        console.log(sqlModal.sql)
        await copy(sqlModal.sql)
    }
}

const { schema, dataProviderInfo } = defineProps<{
    schema: SchemaTablesModel | null,
    dataProviderInfo: DataProviderInfoModel | null
}>()

</script>
