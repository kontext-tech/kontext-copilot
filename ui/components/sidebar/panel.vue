<template>
  <ul class="nav nav-pills flex-column mb-auto flex-fill mt-3">
    <template
      v-for="item in navItems"
      :key="item.id"
    >
      <SidebarNavItem v-bind="item" />
    </template>
  </ul>
</template>

<script setup lang="ts">
import SidebarNavItem from './nav-item.vue';
const config = useAppConfig()
const navItems = config.navItems

</script>

<style lang="scss" scoped></style>
