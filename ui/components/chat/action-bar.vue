<template>
   <BButton
      v-for="(actionModel, i) in props.actions"
      :key="`action-${i}`"
      variant="outline-primary"
      size="sm"
      @click="runAction(actionModel)"
   >
      {{ actionText(actionModel.action) }}
   </BButton>

   <ChatRunSqlModal
      v-model="runSqlModal"
      :sql-statements="sqlStatements"
      @run-sql="runSql"
   ></ChatRunSqlModal>
</template>

<script setup lang="ts">
import { ActionTypes, type ActionModel } from "~/types/Schemas"
import type { RunSqlModalModel } from "~/types/UIProps"

const props = defineProps<{ actions: ActionModel[]; messageId?: number }>()
const emits = defineEmits(["run-sql"])

const runSqlModal = reactive<RunSqlModalModel>({
   open: false,
   sql: ""
})

const sqlStatements = ref<string[]>([])

const actionText = (action: ActionTypes) => {
   switch (action) {
      case ActionTypes.RUN_SQL:
         return "Run SQL"
      default:
         return action
   }
}

const runAction = (actionModel: ActionModel) => {
   if (actionModel.action === ActionTypes.RUN_SQL) {
      if (
         actionModel.data &&
         actionModel.data.sql &&
         Array.isArray(actionModel.data.sql)
      ) {
         sqlStatements.value = actionModel.data.sql.map((d) => String(d))
         runSqlModal.open = true
      }
   }
}

const runSql = () => {
   emits("run-sql", runSqlModal.sql, props.messageId)
}
</script>
