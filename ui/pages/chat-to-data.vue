<template>
    <NuxtLayout>
        <DefaultLayout>
            <template #header-secondary>
                <DataSourceSelector ref="dataSourceSelctor" @data-source-selected="handleDataSourceSelected" />
            </template>
            <template #secondary-sidebar v-if="dataSourceSelctor?.selectedDataSource">
                <DataSourceDisplay :selectedDataSource="dataSourceSelctor.selectedDataSource" />
                <hr>
                <DataProviderDisplay :dataProviderInfo="dataProviderInfo" />
            </template>

            <div class="mt-3 px-4">
                <BAlert variant="secondary" :model-value="!dataSourceSelctor?.selectedDataSource">
                    Please select a data source to start.
                </BAlert>
            </div>
        </DefaultLayout>
    </NuxtLayout>

</template>

<script setup lang="ts">
import DefaultLayout from '~/layouts/default-layout.vue'
import DataSourceSelector from '~/components/data-source/selector.vue'
import type { DataProviderInfoModel } from '~/types/Schemas'
import { DataProviderService } from '~/services/ApiServices'

const dataSourceSelctor = ref<InstanceType<typeof DataSourceSelector> | null>(null)
const dataProviderInfo = ref<DataProviderInfoModel | null>(null)

const appConfig = useAppConfig()
const provideService = new DataProviderService(appConfig.apiBaseUrl)

const handleDataSourceSelected = async (dataSourceId: number) => {
    provideService.getDataProviderInfo(dataSourceId).then((data) => {
        dataProviderInfo.value = data
    }).catch((err) => {
        console.error(err)
    })
}


usePageTitle()
</script>
