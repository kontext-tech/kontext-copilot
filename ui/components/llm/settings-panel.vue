<template>
   <template v-if="settings">
      <div class="d-flex justify-content-between align-items-center">
         <div class="col-md-8">
            <h6>Temperature</h6>
            <span class="text-muted"
               >Higher temperatures lead to more diverse and creative outputs,
               while lower temperatures result in more conservative and
               predictable responses.</span
            >
         </div>
         <div class="col-md-4">
            <BFormInput
               id="temperatureRange"
               v-model="llmTemperature"
               type="range"
               min="0"
               max="1"
               step="0.1"
               number
            />
            {{ llmTemperature }}
         </div>
      </div>
      <hr />
      <div class="d-flex justify-content-between align-items-center">
         <div class="col-md-8">
            <h6>Seed</h6>
            <span class="text-muted"
               >Used to initialize model's random number generator.</span
            >
         </div>
         <div class="col-md-4">
            <BFormInput
               id="seed"
               v-model="llmSeed"
               type="range"
               min="0"
               max="100"
               step="1"
               number
            />
            {{ llmSeed }}
         </div>
      </div>
      <hr />
      <div class="d-flex justify-content-between align-items-center">
         <div class="col-md-8">
            <h6>Top K Sampling (top_k)</h6>
            <span class="text-muted"
               >Limits the generation to the top k most likely next words. The
               model will only consider the top k words with the highest
               probability of occurring next in the sequence.
            </span>
         </div>
         <div class="col-md-4">
            <BFormInput
               id="top_k_range"
               v-model="llmTopK"
               type="range"
               min="0"
               max="100"
               step="1"
               number
            />
            {{ llmTopK }}
         </div>
      </div>
      <hr />
      <div class="d-flex justify-content-between align-items-center">
         <div class="col-md-8">
            <h6>Top P Sampling (top_p)</h6>
            <span class="text-muted"
               >Also known as "nucleus sampling," this parameter filters the
               cumulative distribution of next-word probabilities, so that the
               smallest set of words whose cumulative probability exceeds the
               threshold p is considered.
            </span>
         </div>
         <div class="col-md-4">
            <BFormInput
               id="top_p_range"
               v-model="llmTopP"
               type="range"
               min="0"
               max="1"
               step="0.05"
               number
            />
            {{ llmTopP }}
         </div>
      </div>
      <hr />
      <div class="d-flex justify-content-between align-items-center">
         <div class="col-md-8">
            <h6>Endpoint</h6>
            <span class="text-muted"
               >The endpoint for Ollama or OpenAI compatible LLMs.</span
            >
         </div>
         <div class="col-md-4">
            <BFormInput id="endpoint" v-model="settings.llmEndpoint" />
         </div>
      </div>
      <hr />
      <LlmEndpointSetting />
      <hr />
      <div class="d-flex justify-content-between align-items-center">
         <div class="col-md-8">
            <h6>API key</h6>
            <span class="text-muted"
               >The API key for authenticating with OpenAI services.</span
            >
         </div>
         <div class="col-md-4">
            <BFormInput id="apikey" v-model="llmApiKey" />
         </div>
      </div>
      <hr />
      <div class="d-flex justify-content-between align-items-center">
         <div class="col-md-8">
            <h6>Default model</h6>
            <span class="text-muted">The default model name.</span>
         </div>
         <div class="col-md-4">
            <LlmModelSelector />
         </div>
      </div>
   </template>
</template>

<script setup lang="ts">
const settings = getSettings()

const llmTemperature = computed({
   get: () => settings.value.llmTemperature,
   set: (value) => {
      settings.value.llmTemperature = Number(value)
   }
})

const llmTopK = computed({
   get: () => settings.value.llmTopK,
   set: (value) => {
      settings.value.llmTopK = Number(value)
   }
})

const llmTopP = computed({
   get: () => settings.value.llmTopP,
   set: (value) => {
      settings.value.llmTopP = Number(value)
   }
})

const llmSeed = computed({
   get: () => settings.value.llmSeed,
   set: (value) => {
      settings.value.llmSeed = Number(value)
   }
})

const llmApiKey = computed({
   get: () => settings?.value.llmApiKey ?? "",
   set: (value) => {
      if (settings.value) {
         settings.value.llmApiKey = value
      }
   }
})
</script>
