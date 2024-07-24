<template>
    <NuxtLayout>
        <DefaultLayout>
            <template #header-secondary>
                <DataSourceSelector />
            </template>

        </DefaultLayout>
    </NuxtLayout>

</template>

<script setup lang="ts">
import DefaultLayout from '~/layouts/default-layout.vue'


usePageTitle()
</script>
