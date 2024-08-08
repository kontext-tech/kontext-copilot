<template>
   <DefaultLayout>
      <template #header-secondary>
         <BButton
            variant="outline-secondary"
            size="sm"
            @click="showCreateModal"
         >
            <Icon name="material-symbols:add" /> Add data source
         </BButton>
         <BModal
            :id="createFormModal.id"
            v-model="createFormModal.open"
            :title="createFormModal.title"
            :size="createFormModal.size"
            ok-title="Create"
            @ok.prevent="createDataSource"
            @hidden="resetCreateFormModal"
         >
            <BAlert
               v-if="createFormModal.error"
               :model-value="createFormModal.error != null"
               variant="danger"
            >
               {{ createFormModal.error }}
            </BAlert>
            <DataSourceCreateForm
               v-if="createFormModal.data"
               id="createForm"
               ref="createForm"
               :create-model="createFormModal.data"
            />
         </BModal>
      </template>
      <div class="px-4 mt-3 w-100">
         <DataSourceList
            :data-sources="dataSources"
            @copy="handleCopyDataSource"
            @delete="handleDeleteDataSource"
            @edit="handleEditDataSource"
         />
      </div>
   </DefaultLayout>
</template>

<script setup lang="ts">
import DefaultLayout from "~/layouts/default-layout.vue"
import type { DataSourceCreateModel, DataSourceModel } from "~/types/Schemas"
import DataSourceCreateForm from "~/components/data-source/create-form.vue"
import type { Size } from "bootstrap-vue-next"

const dataSources = ref<DataSourceModel[]>()
const dataSourceService = getDataSourceService()
const createForm = ref<InstanceType<typeof DataSourceCreateForm> | null>(null)
const createFormModal = reactive({
   open: false,
   id: "createFormModal",
   title: "Add data source",
   isLoading: false,
   size: "lg" as Size,
   error: null as string | null,
   data: null as DataSourceCreateModel | null
})

onMounted(() => {
   // Fetch data sources
   dataSourceService
      .getDataSources()
      .then((data) => {
         dataSources.value = data
      })
      .catch((err) => {
         console.error(err)
      })
})

const resetCreateFormModal = () => {
   createFormModal.open = false
   createFormModal.error = null
   createFormModal.data = null
}

const showCreateModal = () => {
   createFormModal.data = {
      type: null,
      name: "",
      conn_str: "",
      description: ""
   }
   createFormModal.open = true
}

// Create data source
const createDataSource = async () => {
   if (createForm.value) {
      const form = createForm.value
      form.setFormEntered(true)
      if (form.formValid) {
         const model = form.model
         try {
            await dataSourceService.createDataSource(model)
            createFormModal.open = false
            dataSources.value = await dataSourceService.getDataSources()
            form.setFormEntered(false)
            resetCreateFormModal()
         } catch (err) {
            createFormModal.error =
               err instanceof Error
                  ? err.message
                  : "An unexpected error occurred"
         }
      }
   }
}

const handleDeleteDataSource = (id: number) => {
   if (dataSources.value) {
      dataSources.value = dataSources.value.filter((ds) => ds.id !== id)
   }
}

const handleEditDataSource = (model: DataSourceModel) => {
   /* find out the model with same id and update its values */
   if (dataSources.value) {
      const index = dataSources.value.findIndex((ds) => ds.id === model.id)
      if (index !== -1) {
         dataSources.value[index] = model
      }
   }
}

const handleCopyDataSource = (model: DataSourceModel) => {
   createFormModal.data = {
      type: model.type,
      name: model.name,
      conn_str: model.conn_str,
      description: model.description
   }
   createFormModal.open = true
}

usePageTitle()
</script>
