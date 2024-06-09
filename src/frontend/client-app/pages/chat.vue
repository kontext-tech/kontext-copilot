<template>
  <div class="header-secondary px-4 border-bottom">
    Chat settings
  </div>
  <div class="chat-main flex-grow-1 flex-shrink-1 px-4">
    Chat content
  </div>

  <div class="chat-input d-flex justify-content-center">
    <div class="input-group">
      <textarea class="form-control chat-textarea" type="text" placeholder="Type a message..." />
      <button class="btn btn-outline-primary" type="button">
        <Icon name="material-symbols:send" size="24" />
      </button>
    </div>
  </div>

</template>

<script setup lang="ts">
definePageMeta({
  title: 'New chat',
})
</script>
<style scoped lang="scss">
@import "../assets/scss/_kontext.scss";
@import "bootstrap/scss/bootstrap";

.chat-input {
  position: fixed;
  bottom: 1rem;
  left: 0;
  margin-inline-start: #{$kontext-sidebar-width};
  padding: 1rem;
  width: calc(100vw - #{$kontext-sidebar-width});

  @include media-breakpoint-down(md) {
    margin-inline-start: 0;
    width: 100%;
  }

  .input-group {
    width: 75%;

    @include media-breakpoint-down(md) {
      width: 100%;
    }
  }

  .chat-textarea {
    max-height: $kontext-chat-input-height;
    overflow-y: auto;
  }
}
</style>