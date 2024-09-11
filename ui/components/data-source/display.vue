<template>
   <div v-if="selectedDataSource">
      <div class="fw-bold mb-3 d-flex align-items-center gap-1">
         <Icon name="material-symbols:database-outline" />
         {{ selectedDataSource.name }}
      </div>
      <BBadge variant="secondary">
         {{ selectedDataSource.type }}
      </BBadge>
      <div class="my-3 text-muted">
         {{ selectedDataSource.description }}

         <span
            v-if="
               selectedDataSource.type === DataSourceType.CSV ||
               selectedDataSource.type === DataSourceType.DuckDB
            "
            class="d-block mt-2"
         >
            <span class="fw-bold">File path:</span> <br />
            <span>{{ selectedDataSource.connStr }}</span>
         </span>
      </div>
   </div>
</template>

<script setup lang="ts">
import { type DataSourceModel, DataSourceType } from "~/types/Schemas"

defineProps<{
   selectedDataSource: DataSourceModel | null
}>()
</script>
