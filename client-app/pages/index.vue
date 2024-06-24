<template>
  <div class="px-4 mt-3">
    <h4>Welcome!</h4>
    <div class="col-md-4">
      <div class="card shadow-sm">
        <div class="card-body">
          <h5 class="card-title">
            Create a chat
          </h5>
          <p class="text-muted">
            Initiate a chat with LLMs.
          </p>
          <NuxtLink to="/chat-ollama" class="btn btn-outline-primary">
            <Icon name="material-symbols:edit-square-outline" /> <span class="ms-1">New chat (Ollama)</span>
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">

usePageTitle()

const btnId = 'btn' + useId()

</script>
