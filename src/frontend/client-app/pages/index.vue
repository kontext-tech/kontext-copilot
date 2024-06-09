<template>
  <div class="px-4">
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
          <NuxtLink to="/chat" class="btn btn-outline-primary">
            <Icon name="material-symbols:edit-square-outline" /> <span class="ms-1">New chat</span>
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">

definePageMeta({
  title: 'Home',
  description: 'This is the home page',
})

const btnId = 'btn' + useId()

</script>
