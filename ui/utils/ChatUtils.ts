import { ChatRole } from "~/types/Schemas"

export const getRoleClass = (role: ChatRole) => {
   switch (role) {
      case ChatRole.USER:
         return "text-primary"
      case ChatRole.ASSISTANT:
         return "text-success"
      default:
         return "text-secondary"
   }
}

export const getRoleIcon = (role: ChatRole) => {
   switch (role) {
      case ChatRole.USER:
         return "material-symbols:person-outline"
      case ChatRole.ASSISTANT:
         return "material-symbols:neurology-outline"
      default:
         return "material-symbols:info-outline"
   }
}

export const getRoleName = (role: ChatRole) => {
   switch (role) {
      case ChatRole.USER:
         return "User"
      case ChatRole.ASSISTANT:
         return "AI Assistant"
      default:
         return "System"
   }
}
