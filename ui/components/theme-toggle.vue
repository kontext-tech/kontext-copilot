<template>
   <BDropdown
      :id="btnId"
      :variant="simple ? 'link' : 'outline-secondary'"
      :disabled="disabled"
   >
      <template #button-content>
         <Icon :name="selectedTheme?.iconName" class="me-1" />
         <template v-if="!simple">
            {{ selectedTheme?.name }}
         </template>
         <Icon name="material-symbols:arrow-drop-down" />
      </template>
      <BDropdownItem
         v-for="theme in themes"
         :key="theme.key"
         :disabled="theme.key === preference"
         @click="setPreference(theme.key)"
      >
         <span class="d-flex align-items-center cursor-pointer">
            <Icon :name="theme.iconName" class="me-1" />
            <span>{{ theme.name }}</span>
            <Icon
               v-if="theme.key === preference"
               name="material-symbols:check"
               class="ms-auto text-primary"
            />
         </span>
      </BDropdownItem>
   </BDropdown>
</template>

<script setup lang="ts">
import type { ThemeConfigItem, ThemeName } from "~/types/Schemas"

const btnId = "btn-theme-toogle-" + useId()
const colorMode = useColorMode({ selector: "html", storageKey: "theme" })
const settings = getSettings()

const preference = computed(() => {
   return settings.value.generalTheme
})
const disabled = computed(() => {
   return !settings
})

watch(preference, (value) => {
   if (value) colorMode.value = value
})

const themes = ref<ThemeConfigItem[]>([
   {
      key: "light",
      name: "Light",
      iconName: "material-symbols:light-mode-outline-rounded"
   },
   {
      key: "dark",
      name: "Dark",
      iconName: "material-symbols:dark-mode-outline-rounded"
   },
   {
      key: "auto",
      name: "System",
      iconName: "material-symbols:computer-outline-rounded"
   }
])

const selectedTheme = computed(() => {
   return (
      themes.value.find((theme) => theme.key === preference.value) ??
      themes.value[0]
   )
})

const setPreference = (mode: ThemeName) => {
   settings.value.generalTheme = mode
}

const { simple } = defineProps<{
   simple?: boolean
}>()
</script>
