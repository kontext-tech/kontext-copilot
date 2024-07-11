<template>
  <NuxtPage />
</template>

<script setup lang="ts">
import _ from 'lodash';
import { SettingsService } from './services/ApiServices';
import type { Settings, SettingsWrapper } from './types/Schemas';

const appConfig = useAppConfig();
const settingsWrapper = ref<SettingsWrapper>({ isLoading: false, loaded: false, error: null, settings: {} as Settings });
const settingsService = new SettingsService(appConfig.apiBaseUrl);

// Function to fetch settings from the API using SettingsService
const fetchSettings = async () => {

  settingsWrapper.value.isLoading = true;
  try {
    settingsWrapper.value.settings = await settingsService.getSettings();
    settingsWrapper.value.error = null;
    settingsWrapper.value.loaded = true;
  } catch (err) {
    settingsWrapper.value.error = err;
    console.log(err);
  } finally {
    settingsWrapper.value.isLoading = false;
  }
};

// Function to update a setting using SettingsService
const setSetting = async (key: string, value: any) => {
  try {
    await settingsService.updateSetting(key, value);
  } catch (err) {
    settingsWrapper.value.error = err;
    console.log(err)
  }
};

watch(() => _.cloneDeep(settingsWrapper.value.settings), async (newSettings, oldSettings) => {
  // Determine what changed and call setSetting for those changes
  let keys: Array<keyof Settings> = Object.keys(newSettings) as Array<keyof Settings>;
  // No need to update to for the initial load
  if (Object.keys(oldSettings).length > 0)
    for (const key of keys) {
      if (oldSettings && newSettings[key] !== oldSettings[key]) {
        console.log("Updating %s=%s", key, newSettings[key])
        await setSetting(key, newSettings[key]);
      }
    }
}, { deep: true });

// Fetch settings on load
fetchSettings();

provide('settings', settingsWrapper);
</script>

<style scoped></style>
