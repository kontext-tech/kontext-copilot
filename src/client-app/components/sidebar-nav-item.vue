<template>
    <li class="nav-item">
        <template v-if="hasChildren">
            <NuxtLink :href="'#' + collapseId" toggle="collapse" class="nav-link d-flex align-items-center mx-2 mb-1"
                :class="{ active: isChildActive }" @click="onClick">
                <Icon :name="icon" size="20" />
                <span class="ms-1">{{ text }}</span>
                <Icon :name="collapseIconName" size="20" class="ms-auto" />
            </NuxtLink>
            <Collapse :key="id" :id="collapseId" ref="collapseEl" :class="collapseClasses">
                <ul class="nav flex-column ms-3">
                    <template v-for="child in props.children">
                        <SidebarNavItem v-bind="child" />
                    </template>
                </ul>
            </Collapse>
        </template>
        <template v-else>
            <NuxtLink :to="to" class="nav-link d-flex align-items-center mx-2 mb-1" :class="{ active: isActive }">
                <Icon :name="icon" size="20" />
                <span class="ms-1">{{ text }}</span>
            </NuxtLink>
        </template>
    </li>
</template>

<script setup lang="ts">
import { ref, watchEffect } from 'vue'
import { useRoute } from 'vue-router'
import type { NavItemProps } from '~/types/UIProps';

const props = defineProps<NavItemProps>()
const route = useRoute()
const isActive = ref(false)
const isChildActive = ref(false)
const hasChildren = computed(() => props.children && props.children?.length > 0)

const collapseEl = ref(null)
const collapseId = 'collapse-' + props.id + useId()

watchEffect(() => {
    isActive.value = route.path === props.to
})

watchEffect(() => {
    isChildActive.value = props.children?.some(child => route.path === child.to) ?? false
})

const collapseClasses = ref(['collapse', "show"])
const collapseShown = ref(true)
const collapseIconName = computed(() => collapseShown.value ? 'material-symbols:keyboard-arrow-up' : 'material-symbols:keyboard-arrow-down')

const onClick = () => {
    collapseShown.value = !collapseShown.value
    collapseClasses.value = collapseShown.value ? ['collapse', "show"] : ['collapse']
}

</script>

<style lang="scss" scoped>
@import '../assets/scss/_kontext.scss';

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