<template>
  <NuxtLayout>
    <DefaultLayout>
      <BTabs
        nav-class="px-4 mt-3 w-100 mb-3"
        content-class="px-4 w-100"
      >
        <BTab
          :id="generalTabId"
          active
        >
          <template #title>
            <span class="d-flex align-items-center">
              <Icon name="material-symbols:settings" /><span class="ms-1">General</span>
            </span>
          </template>
          <div class="d-flex justify-content-between align-items-center">
            <div class="col-md-8">
              <h6>Theme</h6>
              <span class="text-muted">Customize color theme.</span>
            </div>
            <div class="col-md-4">
              <ThemeToggle />
            </div>
          </div>
          <hr>
          <div class="d-flex justify-content-between align-items-center">
            <div class="col-md-8">
              <h6>Name</h6>
              <span class="text-muted">Your name.</span>
            </div>
            <div class="col-md-4">
              <BFormInput
                id="username"
                v-model="settingsWrapper.settings.general_username"
              />
            </div>
          </div>
          <hr>
        </BTab>
        <BTab :id="llmsTabId">
          <template #title>
            <span class="d-flex align-items-center">
              <Icon name="material-symbols:neurology-outline" /><span class="ms-1">LLMs</span>
            </span>
          </template>
          <LlmSettings />
        </BTab>
      </BTabs>
    </DefaultLayout>
  </NuxtLayout>
</template>

<script setup lang="ts">
import DefaultLayout from '~/layouts/default-layout.vue';
import type { SettingsWrapper } from '~/types/Schemas';

const id = useId()
const generalTabId = 'tab-general-' + id
const llmsTabId = 'tab-llms-' + id
const tabContentId = 'tab-content-' + id

usePageTitle()

const settingsWrapper = inject('settings') as Ref<SettingsWrapper>

</script>
