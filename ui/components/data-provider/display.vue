<template>
  <div v-if="dataProviderInfo">
    <div class="fw-bold mb-3 d-flex align-items-center gap-1">
      Objects <BButton
        variant="link"
        class="ms-auto"
        @click="refresh"
      >
        <Icon name="material-symbols:refresh" />
      </BButton>
    </div>
    <!--Loop through schemas-->
    <div class="my-3 text-muted">
      <div
        v-for="(m, index) in dataProviderInfo.metadata"
        :key="index"
      >
        <DataProviderSchemaDisplay
          :schema="m"
          :data-provider-info="dataProviderInfo"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { DataProviderInfoModel } from '~/types/Schemas'

const refresh = () => {
    if (props.dataProviderInfo)
        emits('refresh-clicked', props.dataProviderInfo.id)
}

const emits = defineEmits(['refresh-clicked'])

const props = defineProps<{
    dataProviderInfo: DataProviderInfoModel | null
}>()

</script>
