<template>
    <div class="d-flex justify-content-between align-items-center">
        <div class="col-md-8">
            <h6>Temprature</h6>
            <span class="text-muted">Higher temperatures lead to more diverse and creative outputs, while lower
                temperatures result in more conservative and predictable responses.</span>
        </div>
        <div class="col-md-4">
            <BFormRange id="temperatureRange" v-model="temperature" min="0" max="1" step="0.1" />
            {{ temperature }}
        </div>
    </div>
    <hr>
    <div class="d-flex justify-content-between align-items-center">
        <div class="col-md-8">
            <h6>Endpoint</h6>
            <span class="text-muted">The endpoint for Ollama or OpenAI compatible LLMs.</span>
        </div>
        <div class="col-md-4">
            <BFormInput id="endpoint" v-model="endpoint" />
        </div>
    </div>
    <hr>
    <div class="d-flex justify-content-between align-items-center">
        <div class="col-md-8">
            <h6>API key</h6>
            <span class="text-muted">The API key for authenticating with OpenAI services.</span>
        </div>
        <div class="col-md-4">
            <BFormInput id="apikey" v-model="apikey" />
        </div>
    </div>
    <hr>
    <div class="d-flex justify-content-between align-items-center">
        <div class="col-md-8">
            <h6>Default model</h6>
            <span class="text-muted">The default model name.</span>
        </div>
        <div class="col-md-4">
            <OllamaModelSelector />
        </div>
    </div>
</template>

<script setup lang="ts">
import { useStorage } from '@vueuse/core'

const config = useAppConfig()

const temperature = useStorage(config.settingKeys.llmTemperture, 0.5)
const endpoint = useStorage(config.settingKeys.llmEndpoint, "http://localhost:11434")
const apikey = useStorage(config.settingKeys.llmApiKey, "")
</script>