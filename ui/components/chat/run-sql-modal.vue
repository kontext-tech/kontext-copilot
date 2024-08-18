<template>
   <BModal
      id="runSqlModal"
      v-model="model.open"
      title="Run SQL"
      :size="props.size"
      :ok-disabled="okDisabled"
      @ok="runSql"
   >
      <div
         v-if="sqlStatements.length > 1"
         class="d-flex justify-content-between align-items-center mb-3 gap-3"
      >
         <span class="text-muted flex-shrink-0">Select SQL statement:</span>
         <BFormSelect v-model="model.sql" :options="sqlListOptions" />
      </div>

      <BFormTextarea
         v-model="model.sql"
         rows="10"
         placeholder="Enter SQL statements here"
      />
   </BModal>
</template>
<script setup lang="ts">
import type { Size } from "bootstrap-vue-next"
import type { RunSqlModalModel } from "~/types/UIProps"

const model = defineModel<RunSqlModalModel>({
   default: {
      open: false,
      sql: ""
   }
})
const okDisabled = computed(() => model.value.sql.trim().length === 0)

const runSql = () => {
   if (model.value.sql.trim().length > 0) emits("run-sql")
   model.value.open = false
}

watch(
   () => model.value.open,
   (open) => {
      if (open) {
         model.value.sql = props.sqlStatements[0]
      }
   }
)

const sqlListOptions = computed(() => {
   return props.sqlStatements.map((sql, i) => ({
      value: sql,
      text: `SQL ${i}`
   }))
})

const props = withDefaults(
   defineProps<{ sqlStatements: string[]; size?: Size }>(),
   {
      size: "lg"
   }
)
const emits = defineEmits(["run-sql"])
</script>
