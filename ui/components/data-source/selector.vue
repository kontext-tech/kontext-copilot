<template>
   <BDropdown variant="outline-secondary" size="sm">
      <template #button-content>
         <template v-if="model.model">
            {{ model.model.name }}
         </template>
         <template v-else> Select data source </template>
         <Icon name="material-symbols:arrow-drop-down" />
      </template>
      <BDropdownItem v-if="model.isLoading" disabled>
         Loading...
      </BDropdownItem>
      <BDropdownItem v-if="error">
         {{ error }}
      </BDropdownItem>
      <BDropdownItem
         v-for="ds in dataSources"
         :key="ds.id"
         @click="selectSource(ds)"
      >
         <div class="d-flex align-items-center cursor-pointer">
            <span>{{ ds.name }}</span>
            <BBadge variant="light" class="ms-1">
               {{ ds.type }}
            </BBadge>
            <Icon
               v-if="model.model?.id === ds.id"
               name="material-symbols:check"
               class="ms-auto text-primary"
            />
         </div>
      </BDropdownItem>
   </BDropdown>
</template>

<script setup lang="ts">
import type { DataSourceModel, DataSourceWrapModel } from "~/types/Schemas"

const model = defineModel<DataSourceWrapModel>({
   default: { dataSource: null, isLoading: false, loaded: false }
})

const dataSourceService = getDataSourceService()

const dataSources = ref<DataSourceModel[]>()
const error = ref<string | null>(null)

const selectSource = (ds: DataSourceModel) => {
   model.value.model = ds
   model.value.id = ds.id
   emit("dataSourceSelected", ds.id)
}

const emit = defineEmits(["dataSourceSelected"])

onMounted(() => {
   model.value.isLoading = true
   model.value.loaded = false
   dataSourceService
      .getDataSources()
      .then((data) => {
         dataSources.value = data
         model.value.loaded = true
         model.value.isLoading = false
         if (props.autoSelect && data.length > 0) {
            model.value.model = data[0]
            emit("dataSourceSelected", data[0].id)
         }
      })
      .catch((err) => {
         error.value =
            err instanceof Error ? err.message : "An unexpected error occurred"
         model.value.isLoading = false
         model.value.loaded = false
      })
})

const props = defineProps({
   autoSelect: {
      type: Boolean,
      default: false
   }
})
</script>
