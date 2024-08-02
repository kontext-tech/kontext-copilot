<template>
   <BButtonGroup>
      <BDropdown variant="outline-secondary">
         <template #button-content>
            <template v-if="defaultModel">
               {{ defaultModel.name }}
               {{ defaultModel.details.parameter_size }}
               <Icon name="material-symbols:arrow-drop-down" />
            </template>
            <template v-else> Loading </template>
         </template>
         <BDropdownItem
            v-for="model in models"
            :key="model.name"
            @click="selectModel(model)"
         >
            <div class="d-flex align-items-center cursor-pointer">
               <span>{{ model.name }} {{ model.details.parameter_size }}</span>
               <Icon
                  v-if="defaultModel?.name === model.name"
                  name="material-symbols:check"
                  class="ms-auto text-primary"
               />
            </div>
         </BDropdownItem>
      </BDropdown>
   </BButtonGroup>
</template>

<script setup lang="ts">
import type { ModelResponse } from "ollama/browser"

const { models, defaultModel, setDefaultModel, getModels } = useModels()

const selectModel = (model: ModelResponse) => {
   setDefaultModel(model)
}

onMounted(() => {
   getModels()
})

const selectedModelName = computed(() => defaultModel.value?.name)

defineExpose({
   selectedModelName
})
</script>
