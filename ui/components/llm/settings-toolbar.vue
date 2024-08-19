<template>
   <div
      class="d-flex flex-wrap gap-3 justify-content-center align-items-center"
   >
      <LlmModelSelector v-if="props.modelSelector" />
      <BFormCheckbox
         v-if="props.streamingToggle"
         v-model="model.streaming"
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

const model = defineModel<LlmToolbarOptions>({
   default: {
      streaming: false,
      format: ""
   }
})

watch(jsonFormat, (value) => {
   model.value.format = value ? "json" : ""
})

watchEffect(() => {
   if (defaultModel.value) {
      model.value.model = defaultModel.value.name
   }
})

onMounted(() => {
   if (props.streamingToggle) {
      model.value.streaming =
         props.streamingDefault === undefined ? false : props.streamingDefault
   }
})
</script>
