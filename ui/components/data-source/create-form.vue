<template>
   <div class="container">
      <BForm>
         <BFormGroup
            label="Name"
            label-for="dataSourceName"
            label-class="mb-1"
            class="mb-3"
         >
            <BFormInput
               id="dataSourceName"
               v-model="dataSourceCreateModel.name"
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
               v-model="dataSourceCreateModel.type"
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
               v-model="dataSourceCreateModel.description"
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
               v-model="dataSourceCreateModel.conn_str"
               required
               placeholder="Enter connection string"
               :state="connStrValidation"
            />
            <BFormInvalidFeedback :state="connStrValidation">
               Please input a connection string
            </BFormInvalidFeedback>
         </BFormGroup>

         <!-- <BButton type="submit" variant="primary">Create</BButton> -->
      </BForm>
   </div>
</template>

<script setup lang="ts">
import { DataSourceType, type DataSourceCreateModel } from "~/types/Schemas"

const dataSourceCreateModel = ref<DataSourceCreateModel>({ type: null })
const formEntered = ref(false)
const formValid = computed(
   () => typeValidation.value && nameValidation.value && connStrValidation.value
)

const dataSourceTypes = [
   { value: null, text: "Select the data source type" },
   ...Object.values(DataSourceType).map((type) => ({ value: type, text: type }))
]

const typeValidation = computed(() =>
   !formEntered.value ? null : dataSourceCreateModel.value.type ? true : false
)
const nameValidation = computed(() =>
   !formEntered.value ? null : dataSourceCreateModel.value.name ? true : false
)
const connStrValidation = computed(() =>
   !formEntered.value
      ? null
      : dataSourceCreateModel.value.conn_str
        ? true
        : false
)

const setFormEntered = (status: boolean = true) => {
   formEntered.value = status
}

defineExpose({
   model: dataSourceCreateModel,
   setFormEntered,
   formValid,
   dataSourceCreateModel
})
</script>
