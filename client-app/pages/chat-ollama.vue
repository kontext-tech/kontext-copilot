<template>
  <NuxtLayout>
    <DefaultLayout>
      <template #["header-secondary"]>
        <OllamaModelSelector ref="modelSelector" />
        <BButton button="outline-primary" toggle="modal" target="#llmsSettingsModal">
          <Icon name="material-symbols:neurology-outline" size="20" /> LLMs settings
        </BButton>
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
                <BButton button="secondary" dismiss="modal">
                  Close
                </BButton>
              </ModalFooter>
            </ModalContent>
          </ModalDialog>
        </Modal>
      </template>

      <div class="chat-main p-4 d-flex flex-column gap-4 align-self-center justify-content-center w-75" ref="chatMain">
        <template v-for="message in chatHistory">
          <ChatMessage :message="ollmaMessageToChatMessage(message)" :username="settings.general_username"
            class="w-100" />
        </template>
        <ChatMessage :message="currentResponse" :username="settings.general_username" v-if="generating" class="w-100" />
      </div>

      <div class="chat-input d-flex justify-content-center align-self-center w-75">
        <div class="input-group w-75">
          <textarea ref="chatInput" class="form-control chat-textarea" type="text" v-model="userInput"
            placeholder="Type a message..." @keydown.enter.prevent="sendMessage" :disabled="generating"></textarea>
          <button class="btn btn-outline-primary" type="button" :disabled="sendButtonDisabled" @click="sendMessage">
            <Icon name="material-symbols:send" size="24" />
          </button>
        </div>
      </div>
    </DefaultLayout>
  </NuxtLayout>
</template>


<script setup lang="ts">
import { type Message } from 'ollama/browser'
import ChatMessage from '~/components/chat/chat-message.vue';
import DefaultLayout from '~/layouts/default-layout.vue';
import OllamaLlmService from '~/services/OllamaLlmService';
import { ChatRole, type IChatMessage } from '~/types/Schemas';

const { settings, isLoading, error, } = useSettings()

const userInput = ref<string>('')

const sendButtonDisabled = computed(() => userInput.value.trim().length === 0 || generating.value)

const generating = ref(false)

const chatHistory = ref<Message[]>([])

const currentResponse = ref<IChatMessage>({ role: ChatRole.ASSISTANT, message: '', generating: false })

const chatMain = ref<HTMLElement | null>(null)

const chatInput = ref<HTMLTextAreaElement | null>(null)

const service = new OllamaLlmService(settings.value.llm_endpoint)

const modelSelector = ref()

usePageTitle()

const scrollToBottom = async () => {
  // Scroll to the bottom of the chat-main element
  await nextTick()
  if (chatMain.value && chatMain.value.parentElement) {
    chatMain.value.parentElement.scrollTop = chatMain.value.scrollHeight
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
    model: modelSelector.value?.selectedModelName,
    messages: chatHistory.value,
    stream: true,
    options: { temperature: settings.value.llm_temperature, top_p: settings.value.llm_top_p, top_k: settings.value.llm_top_k, seed: settings.value.llm_seed},
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
  margin-bottom: calc($kontext-chat-input-height + 4*$spacer);
}

.chat-input {
  position: fixed;
  bottom: 0;
  padding-top: calc(2* $spacer);
  padding-bottom: calc(2* $spacer);
  // padding-left: $spacer;
  // padding-right: $spacer;
  width: calc(100vw - #{$kontext-sidebar-width});

  @include media-breakpoint-down(md) {
    margin-inline-start: 0;
    width: 100%;
  }

  .input-group {

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
