<template>
    <ButtonGroup>
        <DropdownToggle button="outline-primary" class="d-flex align-items-center">
            {{ selectedModel?.name }} {{ selectedModel?.details.parameter_size }}
        </DropdownToggle>
        <DropdownMenu alignment="end">
            <DropdownItem v-for="(model, index) in models" @click="selectModel(model)">
                <div class="d-flex align-items-center cursor-pointer">
                    <span>{{ model.name }} {{ model.details.parameter_size }}</span>
                    <Icon v-if="selectedModel?.name === model.name" name="material-symbols:check"
                        class="ms-auto text-primary" />
                </div>
            </DropdownItem>
        </DropdownMenu>
    </ButtonGroup>
</template>

<script setup lang="ts">
import type { ModelResponse } from 'ollama'
import { ref } from 'vue'

const { models, defaultModel, setDefaultModel } = useOllamaModels()
const selectedModel = ref<ModelResponse>()

const selectModel = (model: ModelResponse) => {
    selectedModel.value = model
    selectedModelName.value = model.name
    setDefaultModel(model)
}

const selectedModelName = ref()

watchEffect(() => {
    selectedModel.value = defaultModel.value
})

defineExpose({
    selectedModel,
    selectedModelName
})

</script>