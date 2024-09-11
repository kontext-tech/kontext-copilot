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
            <BFormTextarea
               id="dataSourceConnStr"
               v-model="dataSourceCreateModel.connStr"
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
import { BFormTextarea } from "bootstrap-vue-next"
import { DataSourceType, type DataSourceCreateModel } from "~/types/Schemas"

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
      : dataSourceCreateModel.value.connStr
        ? true
        : false
)

const setFormEntered = (status: boolean = true) => {
   formEntered.value = status
}

const props = defineProps<{
   createModel: DataSourceCreateModel
}>()

const dataSourceCreateModel = ref<DataSourceCreateModel>({
   ...props.createModel
})

watch(
   () => dataSourceCreateModel.value.type,
   (newVal) => {
      if (newVal) {
         if (newVal == DataSourceType.SQLite) {
            dataSourceCreateModel.value.connStr = "sqlite:////path/to/db"
         } else if (newVal == DataSourceType.DuckDB) {
            dataSourceCreateModel.value.connStr = "duckdb:////path/to/db"
         } else if (newVal == DataSourceType.SQLServer) {
            dataSourceCreateModel.value.connStr =
               "mssql+pyodbc://user:password@host:port/databasename?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
         } else if (newVal == DataSourceType.PostgreSQL) {
            dataSourceCreateModel.value.connStr =
               "postgresql+psycopg://user:password@host:port/databasename?key=value&key=value"
         } else if (newVal == DataSourceType.CSV) {
            dataSourceCreateModel.value.connStr = "/path/to/file.csv"
         } else if (newVal == DataSourceType.Parquet) {
            dataSourceCreateModel.value.connStr = "/path/to/file.parquet"
         }
      }
   }
)

defineExpose({
   setFormEntered,
   formValid,
   dataSourceCreateModel,
   model: dataSourceCreateModel
})
</script>
