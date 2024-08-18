<template>
   <template v-for="(actionModel, i) in props.actions" :key="`action-${i}`">
      <BButton
         id="`action-{ i }`"
         v-b-tooltip.click.top="{ title: 'Copied' }"
         variant="outline-primary"
         size="sm"
         @click="runAction(actionModel)"
      >
         {{ actionText(actionModel.action) }}
      </BButton>
      <BTooltip
         v-if="actionModel.action === ActionTypes.COPY_SQL"
         ref="tooltipCopiedSql"
         target="`action-{ i }`"
         placement="top"
         title="Copied"
      >
      </BTooltip>
   </template>

   <ChatRunSqlModal
      v-model="runSqlModal"
      :sql-statements="sqlStatements"
      @run-sql="runSql"
   ></ChatRunSqlModal>
</template>

<script setup lang="ts">
import { ActionTypes, type ActionModel } from "~/types/Schemas"
import type { RunSqlModalModel } from "~/types/UIProps"
import { useClipboard } from "@vueuse/core"

const props = defineProps<{ actions: ActionModel[]; messageId?: number }>()
const emits = defineEmits(["run-sql"])
const { copy } = useClipboard()

const runSqlModal = reactive<RunSqlModalModel>({
   open: false,
   sql: ""
})

const sqlStatements = ref<string[]>([])

const actionText = (action: ActionTypes) => {
   switch (action) {
      case ActionTypes.RUN_SQL:
         return "Run SQL"
      case ActionTypes.COPY_SQL:
         return "Copy SQL"
      default:
         return action
   }
}

const runAction = (actionModel: ActionModel) => {
   switch (actionModel.action) {
      case ActionTypes.RUN_SQL:
         executeRunSqlAction(actionModel)
         break
      case ActionTypes.COPY_SQL:
         executeCopySqlAction(actionModel)
         break
   }
}

const executeCopySqlAction = (actionModel: ActionModel) => {
   if (actionModel.action === ActionTypes.COPY_SQL) {
      if (
         actionModel.data &&
         actionModel.data.sql &&
         typeof actionModel.data.sql === "string"
      ) {
         copy(actionModel.data.sql)
      }
   }
}

const executeRunSqlAction = (actionModel: ActionModel) => {
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
