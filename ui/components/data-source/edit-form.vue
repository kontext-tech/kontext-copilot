<template>
  <div class="container">
    <BForm v-if="updateModel">
      <BFormGroup
        label="Name"
        label-for="dataSourceName"
        label-class="mb-1"
        class="mb-3"
      >
        <BFormInput
          id="dataSourceName"
          v-model="updateModel.name"
          required
          placeholder="Enter data source name"
          :state="nameValidation"
        />
        <BFormInvalidFeedback :state="nameValidation">
          Please input a data source name
        </BFormInvalidFeedback>
      </BFormGroup>

      <BFormGroup
        label="Type"
        label-for="dataSourceType"
        label-class="mb-1"
        class="mb-3"
      >
        <BFormSelect
          id="dataSourceType"
          v-model="updateModel.type"
          :options="dataSourceTypes"
          required
          :state="typeValidation"
        />
        <BFormInvalidFeedback :state="typeValidation">
          Please select a data source type
        </BFormInvalidFeedback>
      </BFormGroup>

      <BFormGroup
        label="Description"
        label-for="dataSourceDesc"
        label-class="mb-1"
        class="mb-3"
      >
        <BFormTextarea
          id="dataSourceDesc"
          v-model="updateModel.description"
        />
      </BFormGroup>

      <BFormGroup
        label="Connection string"
        label-for="dataSourceConnStr"
        label-class="mb-1"
        class="mb-3"
      >
        <BFormInput
          id="dataSourceConnStr"
          v-model="updateModel.conn_str"
          required
          placeholder="Enter connection string"
          :state="connStrValidation"
        />
        <BFormInvalidFeedback :state="connStrValidation">
          Please input a connection string
        </BFormInvalidFeedback>
      </BFormGroup>
    </BForm>
  </div>
</template>

<script setup lang="ts">
import { DataSourceType, type DataSourceUpdateModel } from '~/types/Schemas'
const formEntered = ref(false)
const formValid = computed(() => typeValidation.value && nameValidation.value && connStrValidation.value)

const dataSourceTypes = [
    { value: null, text: 'Select the data source type' },
    ...Object.values(DataSourceType).map((type) => ({ value: type, text: type }))
]

const typeValidation = computed(() => !formEntered.value ? null : props.updateModel?.type ? true : false)
const nameValidation = computed(() => !formEntered.value ? null : props.updateModel?.name ? true : false)
const connStrValidation = computed(() => !formEntered.value ? null : props.updateModel?.conn_str ? true : false)

const setFormEntered = (status: boolean = true) => {
    formEntered.value = status
}

const props = defineProps<{
    updateModel: DataSourceUpdateModel | null
}>()

defineExpose({
    setFormEntered,
    formValid,
})
</script>
