<template>
   <div
      class="d-flex flex-wrap gap-3 justify-content-center align-items-center"
   >
      <LlmModelSelector v-if="props.modelSelector" />
      <BFormCheckbox
         v-if="props.streamingToggle"
         v-model="options.streaming"
         switch
         class="d-flex align-items-center gap-1"
      >
         Streaming
      </BFormCheckbox>
      <BFormCheckbox
         v-if="props.jsonToogle"
         v-model="jsonFormat"
         switch
         class="d-flex align-items-center gap-1"
      >
         JSON format
      </BFormCheckbox>
   </div>
</template>

<script setup lang="ts">
import type { LlmSettingsToolbarProps } from "~/types/UIProps"
import LlmModelSelector from "./model-selector.vue"
import type { LlmToolbarOptions } from "~/types/Schemas"

const props = defineProps<LlmSettingsToolbarProps>()

const jsonFormat = ref(
   props.jsonDefault === undefined ? false : props.jsonDefault
)

const { defaultModel } = useModels()

const options = reactive<LlmToolbarOptions>({
   streaming:
      props.streamingDefault === undefined ? false : props.streamingDefault,
   format: ""
})

watch(jsonFormat, (value) => {
   options.format = value ? "json" : ""
})

watchEffect(() => {
   if (defaultModel.value) {
      options.model = defaultModel.value.name
   }
})

defineExpose(options)
</script>
