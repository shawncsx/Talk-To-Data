<template>
  <div class="chat-input-container border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 p-4">
    <div class="max-w-4xl mx-auto">
      <div class="relative flex items-end gap-2">
        <div class="flex-1 relative">
          <textarea
            v-model="inputText"
            @keydown.enter.prevent="handleEnter"
            @input="adjustHeight"
            ref="textareaRef"
            rows="1"
            placeholder="输入你的问题，例如：查询所有用户的订单总数..."
            class="w-full resize-none rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-3 pr-12 text-gray-900 dark:text-gray-100 placeholder-gray-400 focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20 transition-all"
            :disabled="isLoading"
          ></textarea>
          <button
            v-if="inputText"
            @click="clearInput"
            class="absolute right-3 top-3 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <button
          @click="sendMessage"
          :disabled="!canSend"
          class="flex-shrink-0 h-11 px-4 bg-primary-600 hover:bg-primary-700 disabled:bg-gray-300 dark:disabled:bg-gray-700 disabled:cursor-not-allowed text-white rounded-xl font-medium transition-all flex items-center gap-2"
        >
          <span v-if="isLoading" class="flex items-center gap-2">
            <svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            处理中
          </span>
          <span v-else class="flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
            </svg>
            发送
          </span>
        </button>
      </div>
      
      <div class="mt-2 text-xs text-gray-500 dark:text-gray-400 text-center">
        按 Enter 发送，Shift + Enter 换行
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'

const props = defineProps({
  isLoading: {
    type: Boolean,
    default: false
  },
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['send', 'update:modelValue'])

const inputText = ref(props.modelValue)
const textareaRef = ref(null)

const canSend = computed(() => {
  return inputText.value.trim() && !props.isLoading
})

watch(() => props.modelValue, (newVal) => {
  inputText.value = newVal
})

watch(inputText, (newVal) => {
  emit('update:modelValue', newVal)
})

function adjustHeight() {
  nextTick(() => {
    const textarea = textareaRef.value
    if (textarea) {
      textarea.style.height = 'auto'
      textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px'
    }
  })
}

function handleEnter(event) {
  if (event.shiftKey) {
    // Shift + Enter 换行
    return
  }
  sendMessage()
}

function sendMessage() {
  if (!canSend.value) return
  
  const text = inputText.value.trim()
  if (text) {
    emit('send', text)
    inputText.value = ''
    
    // 重置高度
    nextTick(() => {
      const textarea = textareaRef.value
      if (textarea) {
        textarea.style.height = 'auto'
      }
    })
  }
}

function clearInput() {
  inputText.value = ''
  textareaRef.value?.focus()
}
</script>

<style scoped>
textarea {
  min-height: 44px;
  max-height: 200px;
}
</style>
