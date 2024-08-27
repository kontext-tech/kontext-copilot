import { ActionTypes, ChatRoles } from "~/types/Schemas"

export const getRoleClass = (role: ChatRoles) => {
   switch (role) {
      case ChatRoles.USER:
         return "text-primary"
      case ChatRoles.ASSISTANT:
         return "text-success"
      default:
         return "text-secondary"
   }
}

export const getRoleIcon = (role: ChatRoles) => {
   switch (role) {
      case ChatRoles.USER:
         return "material-symbols:person-outline"
      case ChatRoles.ASSISTANT:
         return "material-symbols:neurology-outline"
      default:
         return "material-symbols:info-outline"
   }
}

export const getRoleName = (role: ChatRoles) => {
   switch (role) {
      case ChatRoles.USER:
         return "User"
      case ChatRoles.ASSISTANT:
         return "Kontext Copilot"
      default:
         return "System"
   }
}

export const getActionName = (action: ActionTypes) => {
   switch (action) {
      case ActionTypes.RUN_SQL:
         return "Run SQL"
      case ActionTypes.COPY_SQL:
         return "Copy SQL"
      case ActionTypes.SQL_TO_PYTHON:
         return "To Python"
      case ActionTypes.SQL_TO_PYSPARK:
         return "To PySpark"
      case ActionTypes.FIX_SQL_ERRORS:
         return "Fix SQL Errors"
      default:
         return action
   }
}
