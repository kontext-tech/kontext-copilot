<template>
  <b-button button="primary" :id="btnId">Primary Button</b-button>
</template>

<script setup lang="ts">

definePageMeta({
  title: 'Home',
  description: 'This is the home page',
})

const btnId = 'btn' + useId()

</script>
