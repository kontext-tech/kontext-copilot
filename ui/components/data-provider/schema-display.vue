<template>
    <BAccordion v-if="schema" free>
        <BAccordionItem :key="schemaName" visible bodyClass="list-group list-group-flush px-0">
            <template #title>
                <h6>
                    <Icon name="material-symbols:schema-outline"></Icon> {{ schemaName }}
                </h6>
            </template>
            <div v-for="(t, index) in schema.tables" :key="index" class="list-group-item d-flex gap-1">
                <span class="flex-grow-1">{{ t }}</span>
                <BLink title="Sample data" @click="showSampleDataModal(t)">
                    <Icon name="material-symbols:data-exploration-outline"></Icon>
                </BLink>
                <BLink title="SQL: creation script" @click="showSqlModal(t)">
                    <Icon name="material-symbols:code"></Icon>
                </BLink>
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
                    <BTable striped hover :items="sampleDataModal.data" :fields="sampleDataFields" />
                </div>
            </BModal>

            <BModal :id="sqlModal.id" :size="sqlModal.size" v-model="sqlModal.open" :title="sqlModal.title"
                :ok-only="true" @hide="resetSqlModal">
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
import type { DataProviderInfoModel, SchemaTablesModel } from '~/types/Schemas'

const schemaName = computed(() => props.schema?.schema ?? "(empty)")

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
        return Object.keys(sampleDataModal.data[0]).map((key) => ({ key, sortable: true }));
    }
    return [];
});

const showSampleDataModal = (table: string) => {
    currentTable.value = table
    /*Load sample data */
    if (props.dataProviderInfo?.id) {
        sampleDataModal.isLoading = true
        dataProviderService.getTableSamples(props.dataProviderInfo.id, table, props.schema?.schema).then((data) => {
            sampleDataModal.data = data
            sampleDataModal.title = currentTable.value ? `Sample data for ${props.schema?.schema ? props.schema.schema + '.' : ''}${currentTable.value}` : "Sample data"
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

const showSqlModal = (table: string) => {
    if (props.dataProviderInfo?.id) {
        sqlModal.isLoading = true
        dataProviderService.getTableCreationSQL(props.dataProviderInfo.id, table, props.schema?.schema).then((data) => {
            sqlModal.title = `CREATE TABLE script for: ${props.schema?.schema ? props.schema.schema + '.' : ''}${table}`
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

const props = defineProps<{
    schema: SchemaTablesModel | null,
    dataProviderInfo: DataProviderInfoModel | null
}>()

</script>
