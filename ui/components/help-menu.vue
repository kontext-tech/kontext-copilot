<template>
   <BDropdown id="help" variant="link">
      <template #button-content>
         <Icon name="material-symbols:help-outline" />
      </template>
      <BDropdownItem
         v-for="item in items"
         :key="item.id"
         :href="item.href"
         target="_blank"
      >
         {{ item.text }}
      </BDropdownItem>
   </BDropdown>
</template>

<script setup lang="ts">
import appConfig from "~/app.config"

const items = [
   {
      id: 1,
      text: "Project site",
      href: appConfig.kontextCopilotUrl
   },
   {
      id: 2,
      text: "LinkedIn",
      href: appConfig.kontextCopilotLinkedInUrl
   }
]
</script>
