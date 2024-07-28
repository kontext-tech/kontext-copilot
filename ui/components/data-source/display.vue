<template>
    <div v-if="selectedDataSource">
        <div class="fw-bold mb-3 d-flex align-items-center gap-1">
            <Icon name="material-symbols:database-outline"></Icon> {{ selectedDataSource.name }}
        </div>
        <BBadge variant="primary">{{ selectedDataSource.type }}</BBadge>
        <div class="my-3 text-muted">{{ selectedDataSource.description }}</div>
    </div>
</template>

<script setup lang="ts">
import type { DataSourceModel } from '~/types/Schemas';

defineProps<{
    selectedDataSource: DataSourceModel | null
}>()

</script>
