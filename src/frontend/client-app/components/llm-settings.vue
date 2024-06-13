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
</template>

<script setup lang="ts">
import { useStorage } from '@vueuse/core'

const config = useAppConfig()

const temperature = useStorage(config.settingKeys.llmTemperture, 0.5);

</script>