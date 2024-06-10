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
            <p>
                {{ message.message }}
            </p>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { ChatMessageProps } from '~/types/UIProps';

const props = defineProps<ChatMessageProps>()

</script>

<style scoped lang="scss">
@import '../../assets/scss/_kontext.scss';
</style>