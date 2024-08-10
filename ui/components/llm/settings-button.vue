<template>
   <BButton
      v-b-modal.llmsSettingsModal
      variant="link"
      size="sm"
      class="d-flex align-items-center"
      title="LLMs settings"
   >
      <Icon name="material-symbols:neurology-outline" size="20" />
   </BButton>
   <BModal id="llmsSettingsModal" title="LLMs settings" ok-only size="lg">
      <LlmSettingsPanel />
   </BModal>
</template>

<script setup lang="ts"></script>
