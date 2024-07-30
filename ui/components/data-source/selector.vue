<template>
  <BDropdown variant="outline-secondary">
    <template #button-content>
      <template v-if="selectedDataSource">
        {{ selectedDataSource.name }}
      </template>
      <template v-else>
        Select data source
      </template>
      <Icon name="material-symbols:arrow-drop-down" />
    </template>
    <BDropdownItem
      v-if="isLoading"
      disabled
    >
      Loading...
    </BDropdownItem>
    <BDropdownItem v-if="error">
      {{ error }}
    </BDropdownItem>
    <BDropdownItem
      v-for="(ds, index) in dataSources"
      :key="ds.id"
      @click="selectSource(ds)"
    >
      <div class="d-flex align-items-center cursor-pointer">
        <span>{{ ds.name }}</span>
        <BBadge
          variant="light"
          class="ms-1"
        >
          {{ ds.type }}
        </BBadge>
        <Icon
          v-if="selectedDataSource?.id === ds.id"
          name="material-symbols:check"
          class="ms-auto text-primary"
        />
      </div>
    </BDropdownItem>
  </BDropdown>
</template>

<script setup lang="ts">
import { DataSourcesService } from '~/services/ApiServices'
import type { DataSourceModel } from '~/types/Schemas'

const appConfig = useAppConfig()
const dataSourcesService = new DataSourcesService(appConfig.apiBaseUrl)
const selectedDataSource = ref<DataSourceModel | null>(null)

const dataSources = ref<DataSourceModel[]>()
const error = ref<string | null>(null)
const isLoading = ref(false)
const loaded = ref(false)

const selectSource = (ds: DataSourceModel) => {
    selectedDataSource.value = ds
    emit('dataSourceSelected', ds.id)
}

const emit = defineEmits(['dataSourceSelected'])

onMounted(() => {
    isLoading.value = true
    loaded.value = false
    dataSourcesService.getDataSources().then((data) => {
        dataSources.value = data
        loaded.value = true
        isLoading.value = false
        if (props.autoSelect && data.length > 0) {
            selectedDataSource.value = data[0]
            emit('dataSourceSelected', data[0].id)
        }
    }).catch((err) => {
        error.value = err instanceof Error ? err.message : 'An unexpected error occurred'
        isLoading.value = false
        loaded.value = false
    })
})

defineExpose({
    selectedDataSource,
})

const props = defineProps({
    autoSelect: {
        type: Boolean,
        default: false
    }
})

</script>
