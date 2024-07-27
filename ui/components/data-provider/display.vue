<template>
    <div v-if="dataProviderInfo">
        <h6>
            Objects
        </h6>
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


defineProps<{
    dataProviderInfo: DataProviderInfoModel | null
}>()

</script>
