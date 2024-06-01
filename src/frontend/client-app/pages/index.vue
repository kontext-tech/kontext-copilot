<script setup lang="ts">
const route = useRoute()
const clicked = () => {
  alert('Button clicked!')
}
</script>

<template>
  <div>
    <p>Current route: {{ route.path }}</p>
  </div>

  <b-button button="primary" @click="clicked"> Primary Button
  </b-button>
</template>
