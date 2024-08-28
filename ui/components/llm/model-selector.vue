<template>
   <BButtonGroup size="sm">
      <BDropdown :variant="simple ? 'link' : 'outline-secondary'" size="sm">
         <template #button-content>
            <template v-if="defaultModel">
               {{ defaultModel.name }}
               {{ defaultModel.details.parameterSize }}
               <Icon name="material-symbols:arrow-drop-down" />
            </template>
            <template v-else> Loading </template>
         </template>
         <BDropdownItem
            v-for="model in models"
            :key="model.name"
            class="border-bottom"
            @click="selectModel(model)"
         >
            <div class="d-flex flex-column cursor-pointer">
               <div class="d-flex gap-3">
                  <span class="fw-bold"
                     >{{ model.name }} {{ model.details.parameterSize }}</span
                  >
                  <Icon
                     v-if="defaultModel?.name === model.name"
                     name="material-symbols:check"
                     class="text-primary"
                  />
               </div>
               <div class="text-muted">
                  family: {{ model.details.family }}; quantization:
                  {{ model.details.quantizationLevel }}; format:
                  {{ model.details.format }}
               </div>
            </div>
         </BDropdownItem>
      </BDropdown>
   </BButtonGroup>
</template>

<script setup lang="ts">
import type { LlmModelResponse } from "~/types/Schemas"

const { models, defaultModel, setDefaultModel, getModels } = useModels()

const selectModel = (model: LlmModelResponse) => {
   setDefaultModel(model)
}

onMounted(() => {
   getModels()
})

const selectedModelName = computed(() => defaultModel.value?.name)

defineExpose({
   selectedModelName
})

defineProps({
   simple: {
      type: Boolean,
      default: false
   }
})
</script>
