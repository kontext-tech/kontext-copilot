<template>
   <BDropdown
      v-if="dataProviderInfo.provider"
      key="schemaSelector"
      variant="outline-secondary"
      :disabled="!dataProviderInfo.provider.supports_schema"
      size="sm"
   >
      <template #button-content>
         <template v-if="selectedSchema">
            {{ selectedSchema }}
         </template>
         <template v-else> Select schema </template>
         <Icon name="material-symbols:arrow-drop-down" />
      </template>
      <BDropdownItem
         v-for="schema in dataProviderInfo.provider.metadata"
         :key="schema.schema ?? '-'"
         @click="handleSelectSchema(schema.schema)"
      >
         {{ schema.schema }}
      </BDropdownItem>
   </BDropdown>

   <BDropdown
      v-if="dataProviderInfo"
      key="tableSelector"
      variant="outline-secondary"
      size="sm"
   >
      <template #button-content>
         <template v-if="selectedTables.length > 0">
            {{ selectedTables.length }} tables selected
         </template>
         <template v-else> Select tables </template>
         <Icon name="material-symbols:arrow-drop-down" />
      </template>
      <BDropdownItem>
         <div
            class="d-flex align-items-center gap-1"
            @change="handleSelectAllTables"
         >
            <BFormCheckbox v-model="selectAll">
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
import type { DataProviderInfoWrapModel } from "~/types/Schemas"

const selectedSchema = ref<string | null>(null)

const handleSelectSchema = (schema: string | null) => {
   if (schema) {
      selectedSchema.value = schema
      emits("schema-changed", schema)
   }
}

const selectedTables = ref<string[]>([])
const tables = computed(() => {
   if (props.dataProviderInfo.provider) {
      const schema = props.dataProviderInfo.provider.supports_schema
         ? props.dataProviderInfo.provider.metadata.find(
              (m) => m.schema === selectedSchema.value
           )
         : props.dataProviderInfo.provider.metadata[0]
      return (
         schema?.tables.map((table) => ({
            key: table,
            label: table,
            selected: selectedTables.value.includes(table)
         })) ?? []
      )
   }
   return []
})

const handleSelectTable = (table: string) => {
   if (selectedTables.value.includes(table)) {
      selectedTables.value = selectedTables.value.filter((t) => t !== table)
   } else {
      selectedTables.value.push(table)
   }
   emits("tables-changed", selectedTables.value)
}
const selectAll = ref(false)
const selectAllLabel = computed(() =>
   selectAll.value ? "Deselect all" : "Select all"
)

const handleSelectAllTables = () => {
   if (!selectAll.value) {
      selectedTables.value = []
      tables.value?.forEach((t) => (t.selected = false))
   } else {
      if (tables.value) {
         selectedTables.value = tables.value.map((t) => t.key)
         tables.value.forEach((t) => (t.selected = true))
      }
   }
   emits("tables-changed", selectedTables.value)
}

const props = defineProps<{
   dataProviderInfo: DataProviderInfoWrapModel
}>()

defineExpose({
   selectedSchema,
   selectedTables
})

const emits = defineEmits(["schema-changed", "tables-changed"])
</script>
