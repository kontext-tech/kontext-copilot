<template>
   <li class="nav-item">
      <template v-if="hasChildren">
         <BLink
            v-b-toggle="collapseId"
            class="nav-link d-flex align-items-center mx-2 mb-1"
            :class="{ active: isChildActive }"
         >
            <Icon :name="icon" size="20" />
            <span class="ms-1">{{ text }}</span>
            <Icon :name="collapseIconName" size="20" class="ms-auto" />
         </BLink>
         <BCollapse
            :id="collapseId"
            :key="id"
            ref="collapseEl"
            visible
            @shown="onCollapseShown"
            @hidden="onCollapseHidden"
         >
            <ul class="nav flex-column ms-3">
               <template v-for="child in props.children" :key="child.id">
                  <SidebarNavItem v-bind="child" />
               </template>
            </ul>
         </BCollapse>
      </template>
      <template v-else>
         <NuxtLink
            :to="to"
            class="nav-link d-flex align-items-center mx-2 mb-1"
            :class="{ active: isActive }"
         >
            <Icon :name="icon" size="20" />
            <span class="ms-1">{{ text }}</span>
         </NuxtLink>
      </template>
   </li>
</template>

<script setup lang="ts">
import type { NavItemProps } from "~/types/UIProps"

const props = defineProps<NavItemProps>()
const route = useRoute()
const isActive = ref(false)
const isChildActive = ref(false)
const hasChildren = computed(() => props.children && props.children?.length > 0)
const collapseId = "collapse-" + props.id

watchEffect(() => {
   isActive.value = route.path === props.to
   isChildActive.value =
      props.children?.some((child) => route.path === child.to) ?? false
})

const isCollapsed = ref(false)
const collapseIconName = computed(() =>
   isCollapsed.value
      ? "material-symbols:keyboard-arrow-down"
      : "material-symbols:keyboard-arrow-up"
)

const onCollapseShown = () => {
   isCollapsed.value = false
}

const onCollapseHidden = () => {
   isCollapsed.value = true
}
</script>

<style lang="scss" scoped>
@import "../assets/scss/_kontext.scss";

.nav-item {
   a {
      color: $text-muted;

      &:hover,
      &.active {
         background-color: $body-tertiary-bg;
         color: $primary-text;
      }
   }
}

/*Dark mode*/
@include color-mode(dark) {
   .nav-item {
      a {
         &:hover,
         &.active {
            background-color: $primary-bg-subtle-dark;
            color: $primary-text-dark;
         }
      }
   }
}
</style>
