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
                  <tr
                     v-for="dataSource in dataSources"
                     :key="`tr-${dataSource.id}`"
                  >
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
                           :key="`${dataSource.id}-btn-copy`"
                           variant="link"
                           title="Copy"
                           @click="copy(dataSource)"
                        >
                           <Icon name="material-symbols:content-copy-outline" />
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
               :id="editModal.id"
               :key="editModal.id"
               v-model="editModal.open"
               :title="editModal.title"
               :size="editModal.size"
               ok-title="Save"
               @ok.prevent="updateDataSource"
               @hide="resetEditModal"
            >
               <BAlert
                  v-if="editModal.error"
                  :model-value="editModal.error != null"
                  variant="danger"
               >
                  {{ editModal.error }}
               </BAlert>
               <EditForm
                  v-if="editModal.data"
                  id="editForm"
                  key="editForm"
                  ref="editForm"
                  :update-model="editModal.data"
               />
            </BModal>
            <BModal
               :id="deleteModal.id"
               :key="deleteModal.id"
               v-model="deleteModal.open"
               :title="deleteModal.title"
               :size="deleteModal.size"
               ok-title="Delete"
               ok-variant="danger"
               @ok.prevent="deleteDataSource"
            >
               <BAlert
                  v-if="deleteModal.error"
                  :model-value="deleteModal.error != null"
                  variant="danger"
               >
                  {{ deleteModal.error }}
               </BAlert>
               <p>Are you sure you want to delete this data source?</p>
               <p><strong>Name:</strong> {{ deleteModal.sourceName }}</p>
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
import type { BModal, Size } from "bootstrap-vue-next"

const dataSourceService = getDataSourceService()

const editForm = ref<InstanceType<typeof EditForm> | null>(null)

const editModal = reactive({
   open: false,
   id: "edit-modal",
   title: "Edit data source",
   isLoading: false,
   error: null as string | null,
   size: "lg" as Size,
   data: null as DataSourceUpdateModel | null,
   sourceId: null as number | null
})
const deleteModal = reactive({
   open: false,
   id: "delete-modal",
   title: "Delete data source",
   isLoading: false,
   error: null as string | null,
   size: "md" as Size,
   sourceName: "" as string,
   sourceId: null as number | null
})

const showDeleteConfirmModal = (model: DataSourceModel) => {
   deleteModal.sourceName = model.name
   deleteModal.sourceId = model.id
   deleteModal.open = true
}

const showEditModal = (model: DataSourceModel) => {
   editModal.data = { ...model }
   editModal.sourceId = model.id
   editModal.open = true
}

const resetEditModal = () => {
   editModal.error = null
   editModal.data = null
   editModal.open = false
   editModal.sourceId = null
}

const deleteDataSource = async () => {
   if (deleteModal.sourceId) {
      try {
         await dataSourceService.deleteDataSource(deleteModal.sourceId)
         // Remove from data sources list
         emit("delete", deleteModal.sourceId)
         deleteModal.open = false
         resetDeleteModal()
      } catch (err) {
         deleteModal.error =
            err instanceof Error ? err.message : "An unexpected error occurred"
         console.error(deleteModal.error)
      }
   }
}

const resetDeleteModal = () => {
   deleteModal.error = null
   deleteModal.sourceName = ""
   deleteModal.sourceId = null
}

const updateDataSource = async () => {
   if (editForm.value) {
      const form = editForm.value
      form.setFormEntered(true)
      if (form.formValid && editModal.sourceId && form.model) {
         try {
            const model = await dataSourceService.updateDataSource(
               editModal.sourceId,
               form.model
            )
            emit("edit", model)
            form.setFormEntered(false)
            resetEditModal()
         } catch (err) {
            editModal.error =
               err instanceof Error
                  ? err.message
                  : "An unexpected error occurred"
            console.error(editModal.error)
         }
      }
   }
}

const copy = (dataSource: DataSourceModel) => {
   emit("copy", dataSource)
}

defineProps<{
   dataSources: DataSourceModel[] | undefined
}>()

const emit = defineEmits<{
   delete: [id: number]
   edit: [model: DataSourceModel]
   copy: [dataSource: DataSourceModel]
}>()
</script>
