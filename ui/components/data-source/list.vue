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
                        <BBadge variant="light">
                           {{ dataSource.type }}
                        </BBadge>
                     </td>
                     <td>{{ dataSource.description }}</td>
                     <td>
                        <BButton
                           :key="`${dataSource.id}-btn-edit`"
                           variant="link"
                           title="Edit"
                           @click="showEditModal(dataSource)"
                        >
                           <Icon name="material-symbols:edit-outline" />
                        </BButton>

                        <BButton
                           :key="`${dataSource.id}-btn-delete`"
                           variant="link"
                           title="Delete"
                           @click="showDeleteConfirmModal(dataSource)"
                        >
                           <Icon name="material-symbols:delete-outline" />
                        </BButton>
                     </td>
                  </tr>
               </tbody>
            </table>
            <BModal
               id="modalEdit"
               key="modalEdit"
               ref="editModal"
               title="Edit data source"
               size="lg"
               ok-title="Save"
               @ok.prevent="updateDataSource"
            >
               <BAlert
                  v-if="error"
                  :model-value="error != null"
                  variant="danger"
               >
                  {{ error }}
               </BAlert>
               <EditForm
                  v-if="currentModel"
                  id="editForm"
                  key="editForm"
                  ref="editForm"
                  :update-model="currentModel"
               />
            </BModal>
            <BModal
               id="modalDelete"
               key="modalDelete"
               ref="deleteConfirmModal"
               title="Delete data source"
               size="md"
               ok-title="Delete"
               ok-variant="danger"
               @ok.prevent="deleteDataSource"
            >
               <BAlert
                  v-if="error"
                  :model-value="error != null"
                  variant="danger"
               >
                  {{ error }}
               </BAlert>
               <p>Are you sure you want to delete this data source?</p>
               <p><strong>Name:</strong> {{ currentModel?.name }}</p>
            </BModal>
         </div>
      </div>
      <div v-else class="alert alert-warning">No data sources found.</div>
   </template>
   <template v-else>
      <div class="w-100 h-100">
         <BSpinner label="Loading data sources..." />
      </div>
   </template>
</template>

<script setup lang="ts">
import type { DataSourceModel, DataSourceUpdateModel } from "~/types/Schemas"
import EditForm from "./edit-form.vue"
import type { BModal } from "bootstrap-vue-next"

const dataSourceService = getDataSourceService()

const currentModel = ref<DataSourceUpdateModel | null>(null)
const currentSourceId = ref<number | null>(null)
const editModal = ref<InstanceType<typeof BModal> | null>(null)
const deleteConfirmModal = ref<InstanceType<typeof BModal> | null>(null)
const editForm = ref<InstanceType<typeof EditForm> | null>(null)
const error = ref<string | null>(null)

const showDeleteConfirmModal = (model: DataSourceModel) => {
   currentModel.value = model
   currentSourceId.value = model.id
   deleteConfirmModal.value?.show()
}

const showEditModal = (model: DataSourceModel) => {
   currentModel.value = model
   currentSourceId.value = model.id
   editModal.value?.show()
}

const deleteDataSource = async () => {
   if (currentSourceId.value) {
      try {
         await dataSourceService.deleteDataSource(currentSourceId.value)
         // Remove from data sources list
         emit("delete", currentSourceId.value)
         deleteConfirmModal.value?.hide()
         currentSourceId.value = null
      } catch (err) {
         error.value =
            err instanceof Error ? err.message : "An unexpected error occurred"
         console.error(error.value)
      }
   }
}

const updateDataSource = async () => {
   if (editForm.value) {
      const form = editForm.value
      form.setFormEntered(true)
      if (form.formValid && currentSourceId.value && form.model) {
         try {
            await dataSourceService.updateDataSource(
               currentSourceId.value,
               form.model
            )
            currentModel.value = null
            form.setFormEntered(false)
            error.value = null
            editModal.value?.hide()
         } catch (err) {
            error.value =
               err instanceof Error
                  ? err.message
                  : "An unexpected error occurred"
            console.error(error.value)
         }
      }
   }
}

defineProps<{
   dataSources: DataSourceModel[] | undefined
}>()

const emit = defineEmits<{
   delete: [id: number]
}>()
</script>
