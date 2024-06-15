<template>
    <ul class="nav nav-pills flex-column mb-auto flex-fill mt-3">
        <template v-for="item in navItems">
            <SidebarNavItem v-bind="item" />
        </template>
    </ul>
</template>

<script setup lang="ts">
import type { NavItemProps } from '~/types/UIProps';
import SidebarNavItem from './sidebar-nav-item.vue';


const navItems = ref<NavItemProps[]>([
  { id: "home", to: '/', icon: 'material-symbols:home-outline', text: 'Home' },
  {
    id: "tools", icon: 'material-symbols:tools-wrench-outline', text: 'LLM Utils', children: [
      { id: "newChat", to: '/chat', icon: 'material-symbols:edit-square-outline', text: 'New chat' },
      { id: "prompt", to: '/prompt-engineering', icon: 'material-symbols:engineering-outline', text: 'Prompt scratchboard' }
    ]
  },
  { id: "llmflow", to: '/dashboards', icon: 'material-symbols:linked-services-outline', text: 'Workflows' },
  { id: "knowledgebase", to: '/dashboards', icon: 'material-symbols:menu-book-outline', text: 'Knowledge base' },
  { id: "dataSources", to: '/data-sources', icon: 'material-symbols:database-outline', text: 'Data sources' },
  // { id: "dataLakes", to: '/data-lakes', icon: 'material-symbols:files-outline', text: 'Datalake' },
  { id: "databoards", to: '/dashboards', icon: 'material-symbols:dashboard-customize-outline', text: 'Dashboards' },
  { id: "settings", to: '/settings', icon: 'material-symbols:settings-outline', text: 'Settings' },
]);


</script>

<style lang="scss" scoped></style>