<template>
    <template v-if="dataSources">
        <div v-if="dataSources.length > 0">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Type</th>
                            <th>Description</th>
                            <th>Options</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="dataSource in dataSources" :key="dataSource.id">
                            <td>{{ dataSource.id }}</td>
                            <td>{{ dataSource.name }}</td>
                            <td>
                                <BBadge variant="light">{{ dataSource.type }}</BBadge>
                            </td>
                            <td>{{ dataSource.description }}</td>
                            <td>
                                <BButton variant="link" title="Edit" :key="`${dataSource.id}-btn`"
                                    @click="showEditModal(dataSource)">
                                    <Icon name="material-symbols:edit-outline" />
                                </BButton>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <BModal title="Edit data source" size="lg" key="modalEdit" id="modalEdit" ok-title="Save"
                    @ok.prevent="updateDataSource" ref="editModal">
                    <BAlert v-if="updateError" :model-value="updateError != null" variant="danger">
                        {{ updateError }}
                    </BAlert>
                    <EditForm id="editForm" :updateModel="currentModel" key="editForm" ref="editForm" />
                </BModal>
            </div>
        </div>
        <div class="alert alert-warning" v-else>
            No data sources found.
        </div>
    </template>
    <template v-else>
        <div class="w-100 h-100">
            <BSpinner label="Loading data sources..." />
        </div>
    </template>

</template>

<script setup lang="ts">
import type { DataSourceModel, DataSourceUpdateModel } from '~/types/Schemas'
import EditForm from './edit-form.vue'
import { DataSourcesService } from '~/services/ApiServices'
import type { BModal } from 'bootstrap-vue-next';

const appConfig = useAppConfig()
const dataSourceService = new DataSourcesService(appConfig.apiBaseUrl)

const currentModel = ref<DataSourceUpdateModel | null>(null)
const currentSourceId = ref<number | null>(null)
const editModal = ref<InstanceType<typeof BModal> | null>(null)
const editForm = ref<InstanceType<typeof EditForm> | null>(null)
const updateError = ref<string | null>(null)

const showEditModal = (model: DataSourceModel) => {
    currentModel.value = model
    currentSourceId.value = model.id
    editModal.value?.show()
}

const updateDataSource = async () => {
    if (editForm.value) {
        const form = editForm.value
        form.setFormEntered(true)
        if (form.formValid && currentSourceId.value && currentModel.value) {
            try {
                await dataSourceService.updateDataSource(currentSourceId.value, currentModel.value)
                form.setFormEntered(false)
                updateError.value = null
                editModal.value?.hide()
            } catch (err) {
                updateError.value = err instanceof Error ? err.message : 'An unexpected error occurred';
                console.error(updateError.value)
            }
        }
    }
}

defineProps<{
    dataSources: DataSourceModel[] | undefined
}>()

</script>
