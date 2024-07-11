<template>
    <ButtonGroup :id="btnId">
        <DropdownToggle button="outline-secondary" class="d-flex align-items-center">
            <Icon :name="preferenceIcon" class="me-1" />
            {{ preferenceText }}
        </DropdownToggle>
        <DropdownMenu alignment="end">
            <DropdownItem key="light" @click="setPreference('light')">
                <div class="d-flex align-items-center cursor-pointer">
                    <Icon name="material-symbols:light-mode-outline" class="me-1" /> <span>Light</span>
                    <Icon v-if="preference === 'light'" name="material-symbols:check" class="ms-auto text-primary" />
                </div>

            </DropdownItem>
            <DropdownItem key="dark" @click="setPreference('dark')">
                <div class="d-flex align-items-center cursor-pointer">
                    <Icon name="material-symbols:dark-mode-outline" class="me-1" /> <span>Dark</span>
                    <Icon v-if="preference === 'dark'" name="material-symbols:check" class="ms-auto text-primary" />
                </div>
            </DropdownItem>
            <DropdownItem key="system" @click="setPreference('system')">
                <div class="d-flex align-items-center cursor-pointer">
                    <Icon name="material-symbols:computer-outline" class="me-1" /> <span>System</span>
                    <Icon v-if="preference === 'system'" name="material-symbols:check" class="ms-auto text-primary" />
                </div>
            </DropdownItem>
        </DropdownMenu>
    </ButtonGroup>
</template>

<script setup lang="ts">
import type { SettingsWrapper } from '~/types/Schemas';

const btnId = 'btn-theme-toogle-' + useId()
const colorMode = useColorMode()
const preference = ref(colorMode.preference)
const settingsWrapper = inject('settings') as Ref<SettingsWrapper>

watch(preference, (value) => {
    colorMode.preference = value
})

const preferenceText = computed(() => {
    switch (colorMode.preference) {
        case 'light':
            return 'Light'
        case 'dark':
            return 'Dark'
        default:
            return 'System'
    }
})

const preferenceIcon = computed(() => {
    switch (colorMode.preference) {
        case 'light':
            return 'material-symbols:light-mode-outline'
        case 'dark':
            return 'material-symbols:dark-mode-outline'
        default:
            return 'material-symbols:computer-outline'
    }
})

const setPreference = (mode: string) => {
    preference.value = mode
    if(settingsWrapper.value) {
        settingsWrapper.value.settings.general_theme = mode
    }
}
</script>
