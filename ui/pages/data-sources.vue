<template>
   <NuxtLayout>
      <DefaultLayout>
         <template #header-secondary>
            <BButton v-b-modal.createFormModal variant="outline-secondary">
               <Icon name="material-symbols:add" /> Add data source
            </BButton>
            <BModal
               id="createFormModal"
               v-model="createFormModal"
               title="Add data source"
               size="lg"
               ok-title="Create"
               @ok.prevent="createDataSource"
            >
               <BAlert
                  v-if="createError"
                  :model-value="createError != null"
                  variant="danger"
               >
                  {{ createError }}
               </BAlert>
               <DataSourceCreateForm id="createForm" ref="createForm" />
            </BModal>
         </template>
         <div class="px-4 mt-3 w-100">
            <DataSourceList
               :data-sources="dataSources"
               @delete="handleDeleteDataSource"
            />
         </div>
      </DefaultLayout>
   </NuxtLayout>
</template>

<script setup lang="ts">
import DefaultLayout from "~/layouts/default-layout.vue"
import type { DataSourceModel } from "~/types/Schemas"
import { DataSourcesService } from "~/services/ApiServices"
import DataSourceCreateForm from "~/components/data-source/create-form.vue"

const appConfig = useAppConfig()
const dataSources = ref<DataSourceModel[]>()
const dataSourceService = new DataSourcesService(appConfig.apiBaseUrl)
const createForm = ref<InstanceType<typeof DataSourceCreateForm> | null>(null)
const createFormModal = ref(false)
const createError = ref<string | null>(null)

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
            form.dataSourceCreateModel = { type: null }
         } catch (err) {
            createError.value =
               err instanceof Error
                  ? err.message
                  : "An unexpected error occurred"
            console.error(createError.value)
         }
      }
   }
}

const handleDeleteDataSource = (id: number) => {
   if (dataSources.value) {
      dataSources.value = dataSources.value.filter((ds) => ds.id !== id)
   }
}

usePageTitle()
</script>
