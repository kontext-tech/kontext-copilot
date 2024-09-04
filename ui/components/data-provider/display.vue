<template>
   <div v-if="dataProviderInfo.model">
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
            v-for="(m, index) in dataProviderInfo.model.metadata"
            v-else
            :key="index"
            class="mb-3"
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
   if (props.dataProviderInfo.model)
      emits("refresh-clicked", props.dataProviderInfo.model.id)
}

const emits = defineEmits(["refresh-clicked"])

const props = defineProps<{
   dataProviderInfo: DataProviderInfoWrapModel
}>()
</script>
