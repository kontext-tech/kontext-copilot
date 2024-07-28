<template>
    <BFormTextarea v-if="dataProviderInfo" class="flex-shrink-0 d-flex flex-column" placeholder="Enter your query here"
        v-model="model.query" rows="6">
    </BFormTextarea>
    <div class="flex-shrink-0">
        <BButton variant="primary" class="mt-3" :disabled="runDisabled" @click="runQuery">
            <Icon name="material-symbols:play-arrow-outline" class="me-1"></Icon>Run
        </BButton>
    </div>
    <div class="flex-grow-1 flex-shrink-1 overflow-y-auto mt-3">
        <BAlert variant="danger" :model-value="hasQueryError">
            <Icon name="material-symbols:error-outline" class="me-1"></Icon>
            <span>{{ model.result?.message }}</span>
        </BAlert>
        <div class="table-responsive" v-if="model.result?.success">
            <BSpinner v-if="model.isLoading" variant="primary"></BSpinner>
            <BTable v-if="!model.isLoading" striped hover small :items="model.result?.data" :fields="tableFields">
            </BTable>
        </div>
    </div>
</template>

<script setup lang="ts">
import { DataProviderService } from '~/services/ApiServices'
import type { DataProviderInfoModel, SqlRunResultModel } from '~/types/Schemas'

const model = reactive({
    query: null as string | null,
    result: null as SqlRunResultModel | null,
    isLoading: false
})

const hasQueryError = computed(() => model.result != null && !model.result.success)

const runDisabled = computed(() => isEmptyOrNull(model.query))

const runQuery = async () => {
    if (dataProviderInfo && model.query) {
        model.isLoading = true
        dataProviderService.getData(dataProviderInfo.id, model.query, selectedSchema).then((result) => {
            model.result = result
            model.isLoading = false
        })
    }
}

const tableFields = computed(() => {
    if (model.result?.data.length > 0) {
        return Object.keys(model.result?.data[0]).map((key) => {
            return { key, label: key, sortable: true }
        })
    }
    return []
})

const appConfig = useAppConfig()
const dataProviderService = new DataProviderService(appConfig.apiBaseUrl)

const { dataProviderInfo, selectedSchema, selectedTables } = defineProps<{
    dataProviderInfo?: DataProviderInfoModel,
    selectedSchema?: string,
    selectedTables?: string[]
}>()

</script>
