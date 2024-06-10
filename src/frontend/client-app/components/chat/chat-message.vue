<template>
    <div class="card mb-3 mx-auto">
        <div class="card-body">
            <div class="card-title d-flex align-items-center">
                <span class="btn rounded-circle d-flex me-1 align-items-center" :class="getRoleClass(message.role)">
                    <Icon :name="getRoleIcon(
                        message.role)" size="24" />
                </span>
                {{ getRoleName(message.role) }}
            </div>
            <p v-html="htmlMessage">
            </p>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { ChatMessageProps } from '~/types/UIProps';
import markdownit from 'markdown-it';

const props = defineProps<ChatMessageProps>()

const md = new markdownit()

const htmlMessage = computed(() => {
    return md.render(props.message.message)
})

</script>

<style scoped lang="scss">
@import '../../assets/scss/_kontext.scss';
</style>