import { ChatRoles } from "~/types/Schemas"

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
         return "AI Assistant"
      default:
         return "System"
   }
}
