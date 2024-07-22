<template>
    <NuxtLayout>
        <DefaultLayout>
            <template #["header-secondary"]>
                <BButton variant="outline-secondary" v-b-modal.createFormModal>
                    <Icon name="material-symbols:add" /> Add data source
                </BButton>
                <BModal v-model="createFormModal" id="createFormModal" title="Add data source" size="lg"
                    okTitle="Create" @ok.prevent="createDataSource">
                    <BAlert v-if="createError" :model-value="createError != null" variant="danger">
                        {{ createError }}
                    </BAlert>
                    <DataSourcesCreateForm ref="createForm" id="createForm" />
                </BModal>
            </template>
            <div class="px-4 mt-3 w-100">
                <DataSourcesList :dataSources="dataSources" />
            </div>
        </DefaultLayout>
    </NuxtLayout>
</template>

<script setup lang="ts">
import DefaultLayout from '~/layouts/default-layout.vue'
import type { DataSourceModel } from '~/types/Schemas'
import { DataSourcesService } from '~/services/ApiServices'
import DataSourcesCreateForm from '~/components/data-sources/data-sources-create-form.vue'

const appConfig = useAppConfig();
const dataSources = ref<DataSourceModel[]>()
const dataSourceService = new DataSourcesService(appConfig.apiBaseUrl)
const createForm = ref<InstanceType<typeof DataSourcesCreateForm> | null>(null)
const createFormModal = ref(false)
const createError = ref<string | null>(null)

onMounted(() => {
    // Fetch data sources
    dataSourceService.getDataSources().then((data) => {
        dataSources.value = data
    }).catch((err) => {
        console.error(err)
    })
})

// Create data source
const createDataSource = async () => {
    if (createForm.value) {
        const form = createForm.value
        form.setFormEntered(true)
        if (form.formValid) {
            const model = form.model
            try {
                await dataSourceService.createDataSource(model)
                createFormModal.value = false
                dataSources.value = await dataSourceService.getDataSources()
                form.setFormEntered(false)
                createError.value = null
            } catch (err) {
                createError.value = err instanceof Error ? err.message : 'An unexpected error occurred';
                console.error(createError.value)
            }
        }
    }

}

usePageTitle()
</script>
