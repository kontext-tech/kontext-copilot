<template>
    <ul class="nav nav-pills flex-column mb-auto flex-fill">
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
    id: "chats", icon: 'material-symbols:chat-outline', text: 'Chat', children: [
      { id: "newChat", to: '/chat', icon: 'material-symbols:edit-square-outline', text: 'New chat' }
    ]
  },
  { id: "settings", to: '/settings', icon: 'material-symbols:settings-outline', text: 'Settings' }
]);


</script>

<style lang="scss" scoped></style>