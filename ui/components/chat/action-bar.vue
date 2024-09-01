<template>
   <template
      v-for="(action, i) in props.actions.actions"
      :key="`action-${props.messageId}-${i}`"
   >
      <BButton
         v-if="action !== ActionTypes.RECOMMEND_CHARTS"
         :id="`action-${props.messageId}-${i}`"
         variant="outline-primary"
         size="sm"
         @click="runAction(action, i)"
      >
         {{ actionText(action) }}
      </BButton>
      <BPopover
         v-if="action === ActionTypes.COPY_SQL"
         :click="true"
         :close-on-hide="true"
         :delay="{ show: 0, hide: 0 }"
         :target="`action-${props.messageId}-${i}`"
         :disabled="popovers.statues[i]"
         placement="top"
         title="Copied!"
         tooltip
         triggers="click"
      >
      </BPopover>
   </template>

   <ChatRunSqlModal
      v-model="runSqlModal"
      :sql-statements="sqlStatements"
      @run-sql="runSql"
   ></ChatRunSqlModal>
</template>

<script setup lang="ts">
import {
   ActionsDataKeys,
   ActionTypes,
   type ActionsModel,
   type RunSqlModalModel
} from "~/types/Schemas"
import { useClipboard } from "@vueuse/core"

const props = defineProps<{ actions: ActionsModel; messageId?: number }>()
const emits = defineEmits(["run-sql", "user-input"])
const { copy } = useClipboard()

const runSqlModal = reactive<RunSqlModalModel>({
   open: false,
   sql: ""
})

const popovers = reactive({
   statues: props.actions.actions.map(() => false)
})

const sqlStatements = ref<string[]>([])

const actionText = (action: ActionTypes) => getActionName(action)

const runAction = (action: ActionTypes, index: number) => {
   switch (action) {
      case ActionTypes.RUN_SQL:
         executeRunSqlAction()
         break
      case ActionTypes.COPY_SQL:
         executeCopySqlAction(index)
         break
      case ActionTypes.SQL_TO_PYTHON:
         executeSqlToPythonAction()
         break
      case ActionTypes.SQL_TO_PYSPARK:
         executeSqlToPysparkAction()
         break
      case ActionTypes.FIX_SQL_ERRORS:
         executeFixSqlErrorsAction()
         break
   }
}

const executeFixSqlErrorsAction = () => {
   if (
      props.actions.data &&
      props.actions.data[ActionsDataKeys.FIX_SQL_ERRORS_PROMPT] &&
      typeof props.actions.data[ActionsDataKeys.FIX_SQL_ERRORS_PROMPT] ===
         "string"
   ) {
      emits(
         "user-input",
         props.actions.data[ActionsDataKeys.FIX_SQL_ERRORS_PROMPT]
      )
   }
}

const executeSqlToPythonAction = () => {
   if (
      props.actions.data &&
      props.actions.data[ActionsDataKeys.SQL_TO_PYTHON_PROMPT] &&
      typeof props.actions.data[ActionsDataKeys.SQL_TO_PYTHON_PROMPT] ===
         "string"
   ) {
      emits(
         "user-input",
         props.actions.data[ActionsDataKeys.SQL_TO_PYTHON_PROMPT]
      )
   }
}

const executeSqlToPysparkAction = () => {
   if (
      props.actions.data &&
      props.actions.data[ActionsDataKeys.SQL_TO_PYSPARK_PROMPT] &&
      typeof props.actions.data[ActionsDataKeys.SQL_TO_PYSPARK_PROMPT] ===
         "string"
   ) {
      emits(
         "user-input",
         props.actions.data[ActionsDataKeys.SQL_TO_PYSPARK_PROMPT]
      )
   }
}

const executeCopySqlAction = (index: number) => {
   if (
      props.actions.data &&
      props.actions.data[ActionsDataKeys.SQL_TEXT] &&
      typeof props.actions.data[ActionsDataKeys.SQL_TEXT] === "string"
   ) {
      copy(props.actions.data[ActionsDataKeys.SQL_TEXT])
      // Dynamically trigger the tooltip
      popovers.statues[index] = true
   }
}

const executeRunSqlAction = () => {
   if (
      props.actions.data &&
      props.actions.data[ActionsDataKeys.SQL_LIST] &&
      Array.isArray(props.actions.data[ActionsDataKeys.SQL_LIST])
   ) {
      sqlStatements.value = props.actions.data[ActionsDataKeys.SQL_LIST].map(
         (d) => String(d)
      )
      runSqlModal.open = true
   }
}

const runSql = () => {
   emits("run-sql", runSqlModal.sql, props.messageId)
}
</script>
