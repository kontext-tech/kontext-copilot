<template>
   <template v-for="(action, i) in props.actions.actions" :key="`action-${i}`">
      <BButton
         id="`action-{ i }`"
         v-b-tooltip.click.top="{ title: 'Copied' }"
         variant="outline-primary"
         size="sm"
         @click="runAction(action)"
      >
         {{ actionText(action) }}
      </BButton>
      <BTooltip
         v-if="action === ActionTypes.COPY_SQL"
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
import { ActionTypes, type ActionsModel } from "~/types/Schemas"
import type { RunSqlModalModel } from "~/types/UIProps"
import { useClipboard } from "@vueuse/core"

const props = defineProps<{ actions: ActionsModel; messageId?: number }>()
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

const runAction = (action: ActionTypes) => {
   switch (action) {
      case ActionTypes.RUN_SQL:
         executeRunSqlAction()
         break
      case ActionTypes.COPY_SQL:
         executeCopySqlAction()
         break
   }
}

const executeCopySqlAction = () => {
   if (
      props.actions.data &&
      props.actions.data.sqlText &&
      typeof props.actions.data.sqlText === "string"
   ) {
      copy(props.actions.data.sqlText)
   }
}

const executeRunSqlAction = () => {
   if (
      props.actions.data &&
      props.actions.data.sql &&
      Array.isArray(props.actions.data.sql)
   ) {
      sqlStatements.value = props.actions.data.sql.map((d) => String(d))
      runSqlModal.open = true
   }
}

const runSql = () => {
   emits("run-sql", runSqlModal.sql, props.messageId)
}
</script>
