<template>
    <div v-if="dataProviderInfo">
        <div class="fw-bold mb-3 d-flex align-items-center gap-1">
            Objects <Icon name="material-symbols:refresh" class="ms-auto cursor-pointer"
                @click="refresh(dataProviderInfo.id)"></Icon>
        </div>
        <!--Loop through schemas-->
        <div class="my-3 text-muted">
            <div v-for="(m, index) in dataProviderInfo.metadata" :key="index">
                <DataProviderSchemaDisplay :schema="m" :data-provider-info="dataProviderInfo" />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { DataProviderInfoModel } from '~/types/Schemas'

const refresh = (dataSourceId: number) => {
    emits('refresh-clicked', dataSourceId)
}

const emits = defineEmits(['refresh-clicked'])

defineProps<{
    dataProviderInfo: DataProviderInfoModel | null
}>()

</script>
