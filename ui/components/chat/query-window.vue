<template>
   <div class="inset-0 h-100 d-flex flex-column align-items-stretch">
      <BFormTextarea
         v-if="dataProviderInfo.model"
         v-model="model.query"
         class="flex-shrink-0 d-flex flex-column"
         placeholder="Enter your query here"
         rows="6"
      />
      <div class="flex-shrink-0">
         <BButton
            variant="primary"
            class="mt-3"
            :disabled="runDisabled"
            @click="runQuery"
         >
            <Icon name="material-symbols:play-arrow-outline" class="me-1" />Run
         </BButton>
      </div>
      <div class="flex-grow-1 flex-shrink-1 overflow-y-auto mt-3">
         <BAlert variant="danger" :model-value="hasQueryError">
            <Icon name="material-symbols:error-outline" class="me-1" />
            <span>{{ model.result?.message }}</span>
         </BAlert>
         <div v-if="model.result?.success" class="table-responsive">
            <BSpinner v-if="model.isLoading" variant="primary" />
            <BTable
               v-if="!model.isLoading"
               striped
               hover
               small
               :items="model.result?.data"
               :fields="tableFields"
            />
            <BAlert
               variant="warning"
               class="d-flex align-items-center"
               :model-value="
                  !model.isLoading &&
                  model.result?.data &&
                  model.result?.data.length == 0
               "
            >
               <Icon name="material-symbols:warning-outline" class="me-1" />
               <span>No records.</span>
            </BAlert>
         </div>
      </div>
   </div>
</template>

<script setup lang="ts">
import type {
   DataProviderInfoWrapModel,
   SqlRunResultModel
} from "~/types/Schemas"

const model = reactive({
   query: null as string | null,
   result: null as SqlRunResultModel | null,
   isLoading: false
})

const hasQueryError = computed(
   () => model.result != null && !model.result.success
)

const runDisabled = computed(() => isEmptyOrNull(model.query))

const runQuery = async () => {
   if (props.dataProviderInfo.model && model.query) {
      model.isLoading = true
      dataProviderService
         .runSql(
            props.dataProviderInfo.model.id,
            model.query,
            props.selectedSchema
         )
         .then((result) => {
            model.result = result
            model.isLoading = false
         })
   }
}

const tableFields = computed(() => {
   if (model.result?.data && model.result?.data.length > 0) {
      return Object.keys(model.result?.data[0]).map((key) => {
         return { key, label: key, sortable: true }
      })
   }
   return []
})

const dataProviderService = getDataProviderService()

const props = defineProps<{
   dataProviderInfo: DataProviderInfoWrapModel
   selectedSchema?: string
   selectedTables?: string[]
}>()
</script>
