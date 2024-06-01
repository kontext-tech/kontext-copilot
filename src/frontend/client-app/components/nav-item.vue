<template>
    <li class="nav-item mb-1">
        <NuxtLink :to="to" class="nav-link d-flex align-items-center">
            <Icon :name="icon" size="24" />
            <span class="ms-2">{{ text }}</span>
        </NuxtLink>
    </li>
</template>

<script setup lang="ts">
interface Props {
    to: string
    icon: string
    text: string
}

const props = defineProps<Props>()
</script>