<template>
  <template v-if="settingsWrapper.isLoading">
    <div class="d-flex justify-content-center align-items-center">
      <BSpinner variant="success" />
    </div>
  </template>
  <template v-else-if="settingsWrapper.error">
    <div class="d-flex align-items-center alert alert-danger">
      <span>{{ settingsWrapper.error }}</span>
    </div>
  </template>
  <template v-if="settings">
    <div class="d-flex justify-content-between align-items-center">
      <div class="col-md-8">
        <h6>Temperature</h6>
        <span class="text-muted">Higher temperatures lead to more diverse and creative outputs, while lower
          temperatures result in more conservative and predictable responses.</span>
      </div>
      <div class="col-md-4">
        <BFormInput
          id="temperatureRange"
          v-model="settings.llm_temperature"
          type="range"
          min="0"
          max="1"
          step="0.1"
        />
        {{ settings.llm_temperature }}
      </div>
    </div>
    <hr>
    <div class="d-flex justify-content-between align-items-center">
      <div class="col-md-8">
        <h6>Seed</h6>
        <span class="text-muted">Used to initialize model's random number generator.</span>
      </div>
      <div class="col-md-4">
        <BFormInput
          id="seed"
          v-model="settings.llm_seed"
          type="range"
          min="0"
          max="100"
          step="1"
        />
        {{ settings.llm_seed }}
      </div>
    </div>
    <hr>
    <div class="d-flex justify-content-between align-items-center">
      <div class="col-md-8">
        <h6>Top K Sampling (top_k)</h6>
        <span class="text-muted">Limits the generation to the top k most likely next words. The model will only
          consider the top k words with the highest probability of occurring next in the sequence. </span>
      </div>
      <div class="col-md-4">
        <BFormInput
          id="top_k_range"
          v-model="settings.llm_top_k"
          type="range"
          min="0"
          max="100"
          step="1"
        />
        {{ settings.llm_top_k }}
      </div>
    </div>
    <hr>
    <div class="d-flex justify-content-between align-items-center">
      <div class="col-md-8">
        <h6>Top P Sampling (top_p)</h6>
        <span class="text-muted">Also known as "nucleus sampling," this parameter filters the cumulative distribution of next-word probabilities, so that the smallest set of words whose cumulative probability exceeds the threshold p is considered. </span>
      </div>
      <div class="col-md-4">
        <BFormInput
          id="top_p_range"
          v-model="settings.llm_top_p"
          type="range"
          min="0"
          max="1"
          step="0.05"
        />
        {{ settings.llm_top_p }}
      </div>
    </div>
    <hr>
    <div class="d-flex justify-content-between align-items-center">
      <div class="col-md-8">
        <h6>Endpoint</h6>
        <span class="text-muted">The endpoint for Ollama or OpenAI compatible LLMs.</span>
      </div>
      <div class="col-md-4">
        <BFormInput
          id="endpoint"
          v-model="settings.llm_endpoint"
        />
      </div>
    </div>
    <hr>
    <div class="d-flex justify-content-between align-items-center">
      <div class="col-md-8">
        <h6>Ollama Endpoint</h6>
        <span class="text-muted">The endpoint for Ollama.</span>
      </div>
      <div class="col-md-4">
        <BFormInput
          id="endpointOllama"
          v-model="settings.llm_ollama_endpoint"
        />
      </div>
    </div>
    <hr>
    <div class="d-flex justify-content-between align-items-center">
      <div class="col-md-8">
        <h6>API key</h6>
        <span class="text-muted">The API key for authenticating with OpenAI services.</span>
      </div>
      <div class="col-md-4">
        <BFormInput
          id="apikey"
          v-model="llmApiKey"
        />
      </div>
    </div>
    <hr>
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
import type { SettingsWrapper } from '~/types/Schemas'

const settingsWrapper = inject('settings') as Ref<SettingsWrapper>
const settings =  computed(() => settingsWrapper.value.settings)


// Handle null values
const llmApiKey = computed({
    get: () => settingsWrapper.value.settings.llm_api_key ?? '',
    set: (value) => {
        if (settingsWrapper.value.loaded) {
            settings.value.llm_api_key = value
        }
    }
})
</script>
