<template>
    <ButtonGroup>
        <DropdownToggle button="outline-primary" class="d-flex align-items-center">
            {{ defaultModel?.name }} {{ defaultModel?.details.parameter_size }}
        </DropdownToggle>
        <DropdownMenu alignment="end">
            <DropdownItem v-for="(model, index) in models" @click="selectModel(model)">
                <div class="d-flex align-items-center cursor-pointer">
                    <span>{{ model.name }} {{ model.details.parameter_size }}</span>
                    <Icon v-if="defaultModel?.name === model.name" name="material-symbols:check"
                        class="ms-auto text-primary" />
                </div>
            </DropdownItem>
        </DropdownMenu>
    </ButtonGroup>
</template>

<script setup lang="ts">
import type { ModelResponse } from 'ollama/browser'

const { models, defaultModel, setDefaultModel } = useOllamaModels()

const selectModel = (model: ModelResponse) => {
    setDefaultModel(model)
}

const selectedModelName = computed(() => defaultModel.value?.name)

defineExpose({
    selectedModelName
})

</script>