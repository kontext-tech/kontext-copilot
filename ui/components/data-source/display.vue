<template>
    <div v-if="selectedDataSource">
        <h6>
            <Icon name="material-symbols:database-outline"></Icon> {{ selectedDataSource.name }}
        </h6>
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
