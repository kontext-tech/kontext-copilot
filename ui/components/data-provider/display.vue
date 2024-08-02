<template>
   <div v-if="dataProviderInfo.provider">
      <div class="fw-bold mb-3 d-flex align-items-center gap-1">
         Objects
         <BButton variant="link" class="ms-auto" @click="refresh">
            <Icon name="material-symbols:refresh" />
         </BButton>
      </div>
      <!--Loop through schemas-->
      <div class="my-3 text-muted">
         <template v-if="props.dataProviderInfo.isLoading">
            <BSpinner variant="primary" />
         </template>
         <div
            v-for="(m, index) in dataProviderInfo.provider.metadata"
            v-else
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
import type { DataProviderInfoWrapModel } from "~/types/Schemas"

const refresh = () => {
   if (props.dataProviderInfo.provider)
      emits("refresh-clicked", props.dataProviderInfo.provider.id)
}

const emits = defineEmits(["refresh-clicked"])

const props = defineProps<{
   dataProviderInfo: DataProviderInfoWrapModel
}>()
</script>
