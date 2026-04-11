<template>
  <div class="app h-screen bg-gray-50 dark:bg-gray-900 flex flex-col overflow-hidden">
    <!-- Header - 固定顶部 -->
    <header class="flex-shrink-0 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <img src="/images/dog.png" alt="Logo" class="h-8 w-8 rounded-lg" />
          <h1 class="text-xl font-bold text-gray-900 dark:text-white">
            飞翔AI <span class="text-primary-600">Talk To Data</span>
          </h1>
        </div>
        
        <div class="flex items-center gap-3">
          <button
            @click="toggleTheme"
            class="p-2 rounded-lg text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          >
            <svg v-if="isDark" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>
            </svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>
            </svg>
          </button>
          
          <button
            @click="chatStore.clearChat"
            v-if="!isAdminPage && chatStore.hasMessages"
            class="px-3 py-1.5 text-sm text-gray-600 dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
          >
            清空对话
          </button>
          
          <button
            @click="isAdminPage = !isAdminPage"
            class="px-3 py-1.5 text-sm text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/20 rounded-lg transition-colors flex items-center gap-1"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
            </svg>
            {{ isAdminPage ? '返回对话' : '后台管理' }}
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content - 占满剩余空间 -->
    <main class="flex-1 overflow-hidden">
      <!-- 对话页面 -->
      <div v-if="!isAdminPage" class="flex h-full overflow-hidden">
        <!-- Sidebar - 固定左侧，内部可滚动 -->
        <aside class="w-80 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col hidden lg:flex overflow-hidden">
          <!-- 可滚动区域 -->
          <div class="flex-1 overflow-y-auto">
            <!-- Sample Questions -->
            <div class="p-4 border-b border-gray-200 dark:border-gray-700">
              <QuestionList
                :questions="chatStore.sampleQuestions"
                title="示例问题"
                :disabled="chatStore.isLoading"
                @select="handleQuestionSelect"
              />
            </div>

            <!-- Follow-up Questions -->
            <div class="p-4 border-b border-gray-200 dark:border-gray-700" v-if="chatStore.followupQuestions.length > 0">
              <QuestionList
                :questions="chatStore.followupQuestions"
                title="跟进问题"
                :disabled="chatStore.isLoading"
                @select="handleQuestionSelect"
              />
            </div>

            <!-- Question History -->
            <div class="p-4">
              <h3 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3 uppercase tracking-wider">
                历史记录
              </h3>
              <div class="space-y-2">
                <button
                  v-for="item in chatStore.questionHistory"
                  :key="item.id"
                  @click="chatStore.loadPreviousQuestion(item.id)"
                  class="w-full text-left p-3 rounded-lg bg-gray-50 dark:bg-gray-800 hover:bg-primary-50 dark:hover:bg-primary-900/20 border border-gray-200 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-700 transition-all group"
                >
                  <p class="text-sm text-gray-700 dark:text-gray-300 group-hover:text-primary-700 dark:group-hover:text-primary-400 line-clamp-2">
                    {{ item.question }}
                  </p>
                  <span class="text-xs text-gray-400 mt-1 block">
                    {{ formatTime(item.timestamp) }}
                  </span>
                </button>
              </div>
              <div v-if="chatStore.questionHistory.length === 0" class="text-center py-4 text-gray-500 text-sm">
                暂无历史记录
              </div>
            </div>
          </div>
        </aside>

        <!-- Chat Area - 中间区域 -->
        <div class="flex-1 flex flex-col bg-gray-50 dark:bg-gray-900 overflow-hidden">
          <!-- Messages - 可滚动区域 -->
          <div ref="messagesContainer" class="flex-1 overflow-y-auto p-4 space-y-4">
            <!-- Welcome Message -->
            <div v-if="!chatStore.hasMessages" class="text-center py-12">
              <div class="max-w-md mx-auto">
                <img src="/images/dog.png" alt="Welcome" class="h-16 w-16 mx-auto mb-4 rounded-2xl" />
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                  欢迎使用 Talk To Data
                </h2>
                <p class="text-gray-600 dark:text-gray-400 mb-6">
                  通过自然语言与数据库对话，轻松查询和分析数据
                </p>
                <div class="flex flex-wrap gap-2 justify-center">
                  <button
                    v-for="question in chatStore.sampleQuestions.slice(0, 3)"
                    :key="question"
                    @click="handleQuestionSelect(question)"
                    class="px-4 py-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-full text-sm text-gray-700 dark:text-gray-300 hover:border-primary-500 hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
                  >
                    {{ question }}
                  </button>
                </div>
              </div>
            </div>

            <!-- Chat Messages -->
            <template v-else>
              <ChatMessage
                v-for="(message, index) in chatStore.messages"
                :key="index"
                :message="message"
                @download="chatStore.downloadCurrentCsv"
                @feedback="chatStore.handleFeedback"
              />
            </template>

            <!-- Loading Indicator -->
            <div v-if="chatStore.isLoading" class="flex justify-center py-4">
              <div class="flex items-center gap-2 text-gray-500">
                <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span class="text-sm">AI 正在思考...</span>
              </div>
            </div>
          </div>

          <!-- Input Area - 固定在底部 -->
          <div class="flex-shrink-0">
            <ChatInput
              v-model="inputText"
              :is-loading="chatStore.isLoading"
              @send="handleSend"
            />
          </div>
        </div>
      </div>

      <!-- 后台管理页面 -->
      <div v-else class="h-full flex overflow-hidden">
        <!-- 左侧菜单栏 -->
        <aside class="w-64 bg-gray-100 dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800">
          <div class="p-4 border-b border-gray-200 dark:border-gray-800">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">后台管理</h3>
          </div>
          <nav class="p-4">
            <ul class="space-y-2">
              <li>
                <button 
                  @click="activeMenu = 'user'"
                  class="w-full text-left px-3 py-2 rounded-lg transition-colors flex items-center gap-2"
                  :class="activeMenu === 'user' ? 'bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400' : 'text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-800'"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                  </svg>
                  用户管理
                </button>
              </li>
              <li>
                <button 
                  @click="activeMenu = 'data-source'"
                  class="w-full text-left px-3 py-2 rounded-lg transition-colors flex items-center gap-2"
                  :class="activeMenu === 'data-source' ? 'bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400' : 'text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-800'"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8-4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"/>
                  </svg>
                  数据源管理
                </button>
              </li>
              <li>
                <button 
                  @click="activeMenu = 'knowledge-base'"
                  class="w-full text-left px-3 py-2 rounded-lg transition-colors flex items-center gap-2"
                  :class="activeMenu === 'knowledge-base' ? 'bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400' : 'text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-800'"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                  </svg>
                  知识库管理
                </button>
              </li>
            </ul>
          </nav>
        </aside>
        
        <!-- 右侧功能区 -->
        <div class="flex-1 overflow-y-auto p-6">
          <!-- 知识库管理 -->
          <div v-if="activeMenu === 'knowledge-base'">
            <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">知识库管理</h2>
            <KnowledgeBase />
          </div>
          
          <!-- 用户管理（暂未实现） -->
          <div v-else-if="activeMenu === 'user'" class="h-full flex items-center justify-center">
            <div class="text-center">
              <div class="text-6xl text-gray-300 dark:text-gray-600 mb-4">
                <svg class="mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24" width="80" height="80">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">功能暂未实现</h3>
              <p class="text-gray-600 dark:text-gray-400">用户管理功能正在开发中，敬请期待</p>
            </div>
          </div>
          
          <!-- 数据源管理 -->
          <div v-else-if="activeMenu === 'data-source'">
            <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">数据源管理</h2>
            <DataSourceManager />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { useChatStore } from '@/stores/chat'
import ChatMessage from '@/components/ChatMessage.vue'
import ChatInput from '@/components/ChatInput.vue'
import QuestionList from '@/components/QuestionList.vue'
import KnowledgeBase from '@/components/KnowledgeBase.vue'
import DataSourceManager from '@/components/DataSourceManager.vue'

const chatStore = useChatStore()
const inputText = ref('')
const messagesContainer = ref(null)
const isDark = ref(false)
const isAdminPage = ref(false)
const activeMenu = ref('knowledge-base')

// Initialize theme
onMounted(() => {
  // Check system preference
  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    isDark.value = true
    document.documentElement.classList.add('dark')
  }
  
  // Load initial data
  chatStore.loadSampleQuestions()
  chatStore.loadQuestionHistory()
})

// Watch messages and scroll to bottom
watch(() => chatStore.messages.length, () => {
  nextTick(() => {
    scrollToBottom()
  })
})

function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

function handleSend(text) {
  chatStore.askQuestion(text)
  inputText.value = ''
}

function handleQuestionSelect(question) {
  inputText.value = question
  handleSend(question)
}

function toggleTheme() {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

function formatTime(timestamp) {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style>
.app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
