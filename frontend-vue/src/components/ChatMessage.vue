<template>
  <div class="chat-message mb-4" :class="messageClass">
    <!-- 用户消息 -->
    <div v-if="message.type === 'user'" class="flex justify-end items-start gap-3">
      <div class="max-w-[70%] bg-primary-600 text-white rounded-2xl rounded-tr-sm px-4 py-3 shadow-sm">
        <p class="text-sm">{{ message.content }}</p>
        <span class="text-xs text-primary-200 mt-1 block text-right">{{ formatTime(message.timestamp) }}</span>
      </div>
      <!-- 用户头像 -->
      <div class="w-10 h-10 flex items-center justify-center flex-shrink-0">
        <svg class="w-10 h-10 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
        </svg>
      </div>
    </div>

    <!-- AI 系统消息（SQL、数据、图表） -->
    <div v-else-if="['sql', 'data', 'chart'].includes(message.type)" class="flex justify-start items-start gap-3">
      <!-- AI 头像 -->
      <div class="w-10 h-10 flex items-center justify-center flex-shrink-0">
        <img src="/images/dog.png" alt="AI" class="w-10 h-10 rounded-lg" />
      </div>
      <div class="max-w-[85%] w-full">
        <!-- SQL 消息 -->
        <div v-if="message.type === 'sql'" class="w-full">
          <SqlDisplay :sql="message.content" />
        </div>
        <!-- 数据表格消息 -->
        <div v-else-if="message.type === 'data'" class="w-full bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4">
          <DataTable 
            :data="message.content" 
            :id="message.id"
            @download="$emit('download', message.id)"
          />
        </div>
        <!-- 图表消息 -->
        <div v-else-if="message.type === 'chart'" class="w-full bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4">
          <ChartDisplay :chart-data="message.content" />
        </div>
      </div>
    </div>

    <!-- 反馈询问消息 -->
    <div v-else-if="message.type === 'feedback'" class="flex justify-start items-start gap-3">
      <!-- AI 头像 -->
      <div class="w-10 h-10 flex items-center justify-center flex-shrink-0">
        <img src="/images/dog.png" alt="AI" class="w-10 h-10 rounded-lg" />
      </div>
      <div class="max-w-[85%] w-full">
        <div class="w-full bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4">
          <p class="text-sm text-gray-700 dark:text-gray-300 mb-3">这些回复内容是否正确？</p>
          <div v-if="!message.answered" class="flex gap-3">
            <button
              @click="$emit('feedback', message.id, true)"
              class="px-4 py-1.5 text-sm bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
            >
              是
            </button>
            <button
              @click="$emit('feedback', message.id, false)"
              class="px-4 py-1.5 text-sm bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
            >
              否
            </button>
          </div>
          <div v-else class="flex items-center gap-2">
            <svg v-if="message.feedback === true" class="w-4 h-4 text-green-600 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
            </svg>
            <svg v-else class="w-4 h-4 text-red-600 dark:text-red-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
            </svg>
            <span class="text-sm text-gray-600 dark:text-gray-400">
              {{ message.feedback === true ? '您认为回复的内容正确' : '您认为回复的内容不正确' }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 反馈结果消息 -->
    <div v-else-if="message.type === 'feedback_result'" class="flex justify-start items-start gap-3">
      <!-- AI 头像 -->
      <div class="w-10 h-10 flex items-center justify-center flex-shrink-0">
        <img src="/images/dog.png" alt="AI" class="w-10 h-10 rounded-lg" />
      </div>
      <div class="max-w-[85%] w-full">
        <div class="w-full bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4">
          <p class="text-sm text-gray-700 dark:text-gray-300">{{ message.content }}</p>
        </div>
      </div>
    </div>

    <!-- 错误消息 -->
    <div v-else-if="message.type === 'error'" class="flex justify-start items-start gap-3">
      <!-- 错误头像 -->
      <div class="w-10 h-10 flex items-center justify-center flex-shrink-0">
        <svg class="w-10 h-10 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
      </div>
      <div class="max-w-[80%] bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg px-4 py-3">
        <div class="flex items-center gap-2 text-red-600 dark:text-red-400">
          <span class="text-sm font-medium">出错了</span>
        </div>
        <p class="text-sm text-red-700 dark:text-red-300 mt-1">{{ message.content }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import SqlDisplay from './SqlDisplay.vue'
import DataTable from './DataTable.vue'
import ChartDisplay from './ChartDisplay.vue'

const props = defineProps({
  message: {
    type: Object,
    required: true
  }
})

defineEmits(['download', 'feedback'])

const messageClass = computed(() => {
  return {
    'user-message': props.message.type === 'user',
    'system-message': props.message.type !== 'user'
  }
})

function formatTime(timestamp) {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleTimeString('zh-CN', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}
</script>

<style scoped>
.chat-message {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
