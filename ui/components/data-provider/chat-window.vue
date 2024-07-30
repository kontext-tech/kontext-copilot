<template>
    <div class="d-flex flex-column h-100 overflow-y-hidden">
        <div class="flex-grow-1 d-flex flex-column overflow-y-hidden vh-100">
            <div class="flex-grow-1 flex-shrink-1 overflow-y-auto" ref="chatMain">
                <template v-for="message in chatHistory">
                    <ChatMessage :message="ollmaMessageToChatMessage(message)" :username="settings.general_username" />
                </template>
                <ChatMessage :message="currentResponse" :username="settings.general_username" v-if="generating" />
            </div>
            <div class="flex-shrink-0 py-4 d-flex align-items-center">
                <span class="chat-icon">
                    <Icon :name="getRoleIcon(
                        ChatRole.USER)" size="24" :class="getRoleClass(ChatRole.USER)" />
                </span>
                <div v-if="settingsWrapper.loaded" class="input-group">
                    <input ref="chatInput" class="form-control" type="text" v-model="userInput"
                        placeholder="Ask a question..." @keydown.enter.prevent="sendMessage"
                        :disabled="generating"></input>
                    <button class="btn btn-primary" type="button" :disabled="sendButtonDisabled" @click="sendMessage">
                        <Icon name="material-symbols:send" size="20" />
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { Message } from 'ollama/browser'
import { DataProviderService } from '~/services/ApiServices'
import OllamaLlmService from '~/services/OllamaLlmService';
import { ChatRole, type DataProviderInfoModel, type IChatMessage, type SettingsWrapper } from '~/types/Schemas'

const settingsWrapper = inject('settings') as Ref<SettingsWrapper>
const settings = computed(() => settingsWrapper.value.settings)
const loaded = computed(() => settingsWrapper.value.loaded)

const appConfig = useAppConfig()
const dataProviderService = new DataProviderService(appConfig.apiBaseUrl)

const userInput = ref<string>('')

const sendButtonDisabled = computed(() => userInput.value.trim().length === 0 || generating.value)

const generating = ref(false)

const chatHistory = ref<Message[]>([])

const chatMain = ref<HTMLElement | null>(null)

const chatInput = ref<HTMLTextAreaElement | null>(null)

const currentResponse = ref<IChatMessage>({ role: ChatRole.ASSISTANT, message: '', generating: false })

const scrollToBottom = async () => {
    // Scroll to the bottom of the chat-main element
    await nextTick()
    if (chatMain.value) {
        chatMain.value.scrollTop = chatMain.value.scrollHeight
    }
    if (chatInput.value) {
        chatInput.value.focus()
    }
}

let ollamaService: OllamaLlmService
const getOllamaService = () => {
    if (!ollamaService && loaded.value) {
        ollamaService = new OllamaLlmService(settingsWrapper.value.settings.llm_endpoint)
    }
    return ollamaService
}

const sendMessage = async () => {
    generating.value = true
    chatHistory.value.push({ role: 'user', content: userInput.value })
    userInput.value = ''
    await scrollToBottom()
    currentResponse.value.generating = true
    const oService = getOllamaService()
    if (props.selectedModelName === undefined)
        return
    const response = await oService.ollama.chat({
        model: props.selectedModelName,
        messages: chatHistory.value,
        stream: true,
        options: { temperature: settings.value.llm_temperature, top_p: settings.value.llm_top_p, top_k: settings.value.llm_top_k, seed: settings.value.llm_seed },
    })
    for await (const part of response) {
        currentResponse.value.message += part.message.content
        await scrollToBottom()
        if (part.done) {
            chatHistory.value.push({ role: 'assistant', content: currentResponse.value.message || '' })
            generating.value = false
            /* Reset the value */
            currentResponse.value.message = ""
            await scrollToBottom()
        }
    }

}

const props = defineProps<{
    dataProviderInfo?: DataProviderInfoModel,
    selectedSchema?: string,
    selectedTables?: string[],
    selectedModelName?: string
}>()

</script>
