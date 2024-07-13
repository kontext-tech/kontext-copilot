<template>
    <BButtonGroup :id="btnId" :disabled="disabled">
        <BDropdown variant="outline-secondary">
            <template #button-content>
                <Icon :name="preferenceIcon" />
                {{ preferenceText }}
                <Icon name="material-symbols:arrow-drop-down" />
            </template>
            <BDropdownItem key="light" @click="setPreference('light')" :disabled="preference === 'light'">
                <span class="d-flex align-items-center cursor-pointer">
                    <Icon name="material-symbols:light-mode-outline-rounded" class="me-1" /> <span>Light</span>
                    <Icon v-if="preference === 'light'" name="material-symbols:check" class="ms-auto text-primary" />
                </span>
            </BDropdownItem>
            <BDropdownItem key="dark" @click="setPreference('dark')" :disabled="preference === 'dark'">
                <span class="d-flex align-items-center cursor-pointer">
                    <Icon name="material-symbols:dark-mode-outline-rounded" class="me-1" /> <span>Dark</span>
                    <Icon v-if="preference === 'dark'" name="material-symbols:check" class="ms-auto text-primary" />
                </span>
            </BDropdownItem>
            <BDropdownItem key="auto" @click="setPreference('auto')" :disabled="preference === 'auto'">
                <span class="d-flex align-items-center cursor-pointer">
                    <Icon name="material-symbols:computer-outline-rounded" class="me-1" /> <span>System</span>
                    <Icon v-if="preference === 'auto'" name="material-symbols:check" class="ms-auto text-primary" />
                </span>
            </BDropdownItem>
        </BDropdown>
    </BButtonGroup>
</template>

<script setup lang="ts">
import type { SettingsWrapper } from '~/types/Schemas';

const btnId = 'btn-theme-toogle-' + useId()
const colorMode = useColorMode({ selector: 'html', storageKey: 'theme' })
const settingsWrapper = inject('settings') as Ref<SettingsWrapper>
const preference = computed(() => {
    return settingsWrapper.value.settings.general_theme
})
const disabled = computed(() => {
    return settingsWrapper.value.loaded === false
})

watch(preference, (value) => {
    colorMode.value = value
})

const preferenceText = computed(() => {
    switch (preference.value) {
        case 'light':
            return 'Light'
        case 'dark':
            return 'Dark'
        default:
            return 'System'
    }
})

const preferenceIcon = computed(() => {
    switch (preference.value) {
        case 'light':
            return 'material-symbols:light-mode-outline-rounded'
        case 'dark':
            return 'material-symbols:dark-mode-outline-rounded'
        default:
            return 'material-symbols:computer-outline-rounded'
    }
})

const setPreference = (mode: "dark" | "light" | "auto") => {
    if (settingsWrapper.value) {
        settingsWrapper.value.settings.general_theme = mode
    }
}
</script>
