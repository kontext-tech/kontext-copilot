import { ref, onMounted, watch } from 'vue';
import { SettingsService } from '~/services/ApiServices';
import { type Settings } from '~/types/Schemas';
import _ from 'lodash';

export function useSettings() {
    const settingsService = new SettingsService();
    const settings = ref<Settings>({} as Settings);
    const isLoading = ref(true);
    const loaded = ref(false);
    const error = ref<any>(null);

    // Function to fetch settings from the API using SettingsService
    const fetchSettings = async () => {
        isLoading.value = true;
        try {
            settings.value = await settingsService.getSettings();
            error.value = null;
        } catch (err) {
            error.value = err;
            console.log(err);
        } finally {
            isLoading.value = false;
        }
    };

    // Function to update a setting using SettingsService
    const setSetting = async (key: string, value: any) => {
        try {
            await settingsService.updateSetting(key, value);
        } catch (err) {
            error.value = err;
            console.log(err)
        }
    };

    watch(() => _.cloneDeep(settings.value), async (newSettings, oldSettings) => {
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

    // Fetch settings when the component using this composable is mounted
    onMounted(fetchSettings);

    return { settings, isLoading, error, setSetting };
}
