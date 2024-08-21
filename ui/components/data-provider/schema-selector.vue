<template>
   <BDropdown
      v-if="dataProviderInfo.model"
      key="schemaSelector"
      variant="outline-secondary"
      :disabled="!dataProviderInfo.model.supportsSchema"
      size="sm"
   >
      <template #button-content>
         <template v-if="model.schema">
            {{ model.schema }}
         </template>
         <template v-else> Select schema </template>
         <Icon name="material-symbols:arrow-drop-down" />
      </template>
      <BDropdownItem
         v-for="schema in dataProviderInfo.model.metadata"
         :key="schema.schemaName ?? '-'"
         @click="handleSelectSchema(schema.schemaName)"
      >
         {{ schema.schemaName }}
      </BDropdownItem>
   </BDropdown>

   <BDropdown
      v-if="dataProviderInfo.model"
      key="tableSelector"
      variant="outline-secondary"
      size="sm"
   >
      <template #button-content>
         <template v-if="model.tables.length > 0">
            {{ model.tables.length }} tables selected
         </template>
         <template v-else> Select tables </template>
         <Icon name="material-symbols:arrow-drop-down" />
      </template>
      <BDropdownItem>
         <div
            class="d-flex align-items-center gap-1"
            @change="handleSelectAllTables"
         >
            <BFormCheckbox v-model="model.selectAll">
               {{ selectAllLabel }}
            </BFormCheckbox>
         </div>
      </BDropdownItem>
      <BDropdownItem
         v-for="table in tables"
         :key="table.key"
         @click="handleSelectTable(table.key)"
      >
         <div class="d-flex align-items-center gap-1">
            <BFormCheckbox :key="table.key" v-model="table.selected" />
            <Icon name="material-symbols:table" /> {{ table.label }}
         </div>
      </BDropdownItem>
   </BDropdown>
</template>

<script setup lang="ts">
import type {
   DataProviderInfoWrapModel,
   SchemaSelectorModel
} from "~/types/Schemas"

const model = defineModel<SchemaSelectorModel>({
   default: { schema: undefined, tables: [], selectAll: false }
})

const handleSelectSchema = (schema: string | null) => {
   if (schema) {
      model.value.schema = schema
      // Reset selected tables
      model.value.tables = []
   }
}

const tables = computed(() => {
   if (props.dataProviderInfo.model) {
      const schema = props.dataProviderInfo.model.supportsSchema
         ? props.dataProviderInfo.model.metadata.find(
              (m) => m.schemaName === model.value.schema
           )
         : props.dataProviderInfo.model.metadata[0]
      return (
         schema?.tables.map((table) => ({
            key: table,
            label: table,
            selected: model.value.tables.includes(table)
         })) ?? []
      )
   }
   return []
})

const handleSelectTable = (table: string) => {
   const index = model.value.tables.indexOf(table)
   if (index !== -1) {
      model.value.tables.splice(index, 1)
   } else {
      model.value.tables.push(table)
   }
}

const selectAllLabel = computed(() =>
   model.value.selectAll ? "Deselect all" : "Select all"
)

const handleSelectAllTables = () => {
   if (!model.value.selectAll) {
      model.value.tables = []
      tables.value?.forEach((t) => (t.selected = false))
   } else {
      if (tables.value) {
         model.value.tables = tables.value.map((t) => t.key)
         tables.value.forEach((t) => (t.selected = true))
      }
   }
}

const props = defineProps<{
   dataProviderInfo: DataProviderInfoWrapModel
}>()
</script>
