<template>
    <template v-if="isLoading">
        <div class="d-flex justify-content-center align-items-center">
            <Spinner />
        </div>
    </template>
    <template v-else-if="error">
        <div class="d-flex align-items-center alert alert-danger">
            <span>{{ error }}</span>
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
                <BFormRange id="temperatureRange" v-model="settings.llm_temperature" min="0" max="1" step="0.1" />
                {{ settings.llm_temperature }}
            </div>
        </div>
        <hr>
        <div class="d-flex justify-content-between align-items-center">
            <div class="col-md-8">
                <h6>Endpoint</h6>
                <span class="text-muted">The endpoint for Ollama or OpenAI compatible LLMs.</span>
            </div>
            <div class="col-md-4">
                <BFormInput id="endpoint" v-model="settings.llm_endpoint" />
            </div>
        </div>
        <hr>
        <div class="d-flex justify-content-between align-items-center">
            <div class="col-md-8">
                <h6>API key</h6>
                <span class="text-muted">The API key for authenticating with OpenAI services.</span>
            </div>
            <div class="col-md-4">
                <BFormInput id="apikey" v-model="llmApiKey" />
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
</template>

<script setup lang="ts">
import { useSettings } from '~/composables/useSettings'

const { settings, isLoading, error, } = useSettings()

// Handle null values
const llmApiKey = computed({
    get: () => settings.value?.llm_api_key ?? '',
    set: (value) => {
        if (settings.value) {
            settings.value.llm_api_key = value
        }
    }
})
</script>
