<template>
  <BButton
    v-b-modal.llmsSettingsModal
    variant="outline-secondary"
    class="d-flex align-items-center"
  >
    <Icon
      name="material-symbols:neurology-outline"
      size="20"
    /> LLMs settings
  </BButton>
  <BModal
    id="llmsSettingsModal"
    title="LLMs settings"
    ok-only
    size="lg"
  >
    <LlmSettings />
  </BModal>
</template>

<script setup lang="ts">
</script>
