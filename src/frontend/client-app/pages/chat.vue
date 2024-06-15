<template>
  <div class="header-secondary px-4 border-bottom d-grid gap-2 d-flex align-items-center">
    <OllamaModelSelector ref="modelSelector" />
    <b-button button="outline-primary" toggle="modal" target="#llmsSettingsModal">
      <Icon name="material-symbols:neurology-outline" size="20" /> LLMs settings
    </b-button>
  </div>
  <Modal id="llmsSettingsModal">
    <ModalDialog class="modal-lg">
      <ModalContent>
        <ModalHeader>
          <ModalTitle>LLMs settings</ModalTitle>
          <CloseButton dismiss="modal" />
        </ModalHeader>
        <ModalBody>
          <LlmSettings />
        </ModalBody>
        <ModalFooter>
          <b-button button="secondary" dismiss="modal">
            Close
          </b-button>
        </ModalFooter>
      </ModalContent>
    </ModalDialog>
  </Modal>
  <div class="chat-main d-flex flex-column justify-content-center overflow-y-auto" ref="chatMain">
    <template v-for="message in chatHistory">
      <ChatMessage :message="ollmaMessageToChatMessage(message)" />
    </template>
    <ChatMessage :message="currentResponse" v-if="generating" />
  </div>

  <div class="chat-input d-flex justify-content-center bg-opacity-75">
    <div class="input-group">
      <textarea ref="chatInput" class="form-control chat-textarea" type="text" v-model="userInput"
        placeholder="Type a message..." @keydown.enter.prevent="sendMessage" :disabled="generating"></textarea>
      <button class="btn btn-outline-primary" type="button" :disabled="sendButtonDisabled" @onclick="sendMessage">
        <Icon name="material-symbols:send" size="24" />
      </button>
    </div>
  </div>

</template>

<script setup lang="ts">
import { type Message } from 'ollama'
import ChatMessage from '~/components/chat/chat-message.vue';
import OllamaLlmService from '~/services/OllamaLlmService';
import { ChatRole, type IChatMessage } from '~/types/Models';

const userInput = ref<string>('')

const sendButtonDisabled = computed(() => userInput.value.trim().length === 0 || generating.value)

const generating = ref(false)

const chatHistory = ref<Message[]>([])

const currentResponse = ref<IChatMessage>({ role: ChatRole.ASSISTANT, message: '', generating: false })

const chatMain = ref<HTMLElement | null>(null)

const chatInput = ref<HTMLTextAreaElement | null>(null)

const service = new OllamaLlmService()

const modelSelector = ref<any>(null)

definePageMeta({
  title: 'New chat',
})

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

/* Send user input and getting response */
const sendMessage = async () => {
  generating.value = true
  chatHistory.value.push({ role: 'user', content: userInput.value })
  userInput.value = ''
  await scrollToBottom()
  currentResponse.value.generating = true

  const response = await service.ollama.chat({
    model: modelSelector.value?.selectedModelName || 'llama3',
    messages: chatHistory.value,
    stream: true,
    options: { temperature: service.temperature },
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

</script>


<style scoped lang="scss">
@import "../assets/scss/_kontext.scss";
@import "bootstrap/scss/bootstrap";

.chat-main {
  overflow-y: auto;
  // margin-top: 1rem;
  padding: 1rem;
  // padding-top: calc(2 * #{$spacer} + #{$kontext-header-height});
  max-height: calc(100vh - 2 * #{$kontext-header-height} - #{$spacer} - #{$kontext-chat-input-height} - 4 * #{$spacer});
  height: calc(100vh - 2 * #{$kontext-header-height} - #{$spacer} - #{$kontext-chat-input-height} - 4 * #{$spacer});

  .card {
    width: 75% !important;
  }

  @include media-breakpoint-down(md) {
    max-height: calc(100vh - 2 * #{$kontext-header-height} - #{$kontext-chat-input-height} - 1rem);

    .card {
      width: 100% !important;
    }
  }
}

.chat-input {
  position: fixed;
  bottom: 0;
  left: 0;
  margin-inline-start: #{$kontext-sidebar-width};
  padding-top: calc(2* $spacer);
  padding-bottom: calc(2* $spacer);
  padding-left: $spacer;
  padding-right: $spacer;
  width: calc(100vw - #{$kontext-sidebar-width});

  @include media-breakpoint-down(md) {
    margin-inline-start: 0;
    width: 100%;
  }

  .input-group {
    width: 75%;

    @include media-breakpoint-down(md) {
      width: 100%;
      padding-left: $spacer;
      padding-right: $spacer;
    }
  }

  .chat-textarea {
    max-height: $kontext-chat-input-height;
    height: $kontext-chat-input-height;
    overflow-y: auto;
  }
}
</style>