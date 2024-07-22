<template>
    <BButton variant="outline-secondary" v-b-modal.llmsSettingsModal class="d-flex align-items-center">
        <Icon name="material-symbols:neurology-outline" size="20" /> LLMs settings
    </BButton>
    <BModal id="llmsSettingsModal" title="LLMs settings" okOnly size="lg">
        <LlmSettings />
    </BModal>
</template>

<script setup lang="ts">
</script>
