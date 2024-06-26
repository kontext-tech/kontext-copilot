<template>
    <div class="card shadow-sm">
        <div class="card-body">
            <div class="card-title d-flex align-items-center">
                <span class="btn rounded-circle d-flex me-1 align-items-center" :class="getRoleClass(message.role)">
                    <Icon :name="getRoleIcon(
                        message.role)" size="24" />
                </span>
                <strong v-if="message.role === ChatRole.USER">{{ username }}</strong>
                <strong v-else>{{ getRoleName(message.role) }}</strong>
            </div>
            <div v-html="htmlMessage">
            </div>
            <div v-if="!message.generating">
                <span class="text-muted cursor-pointer" @click="copyMessage">
                    <Icon name="material-symbols:content-copy-outline" size="18"  />
                </span>
            </div>
        </div>

    </div>
</template>

<script setup lang="ts">
import type { ChatMessageProps } from '~/types/UIProps';
import markdownit from 'markdown-it';
import useClipboard from 'vue-clipboard3'
import { ChatRole } from '~/types/Models';

const props = defineProps<ChatMessageProps>()

const username = useUsername()

const md = new markdownit()

const htmlMessage = computed(() => {
    if (props.message.generating && props.message.message === "")
        return "<em>Thinking...</em>"
    return md.render(props.message.message)
})

const { toClipboard } = useClipboard()

const copyMessage = async () => {
    await toClipboard(props.message.message);
}

</script>

<style scoped lang="scss">
@import '../../assets/scss/_kontext.scss';
</style>