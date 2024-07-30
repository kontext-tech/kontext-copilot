<template>
  <NuxtLayout>
    <DefaultLayout>
      <div class="px-4 mt-3 w-100">
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
              <NuxtLink
                to="/chat"
                class="btn btn-outline-primary"
              >
                <Icon name="material-symbols:edit-square-outline" /> <span>New chat</span>
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </DefaultLayout>
  </NuxtLayout>
</template>

<script setup lang="ts">
import DefaultLayout from '~/layouts/default-layout.vue'
usePageTitle()

const btnId = 'btn' + useId()

</script>
