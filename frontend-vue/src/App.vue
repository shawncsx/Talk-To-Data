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
            <!-- 数据源选择器 -->
            <div class="p-4 border-b border-gray-200 dark:border-gray-700">
              <h3 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3 uppercase tracking-wider">
                选择数据源
              </h3>
              <select
                v-model="selectedDataSourceId"
                @change="handleDataSourceChange"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option v-for="source in dataSources" :key="source.id" :value="source.id">
                  {{ source.name }} ({{ source.type === 'mysql' ? 'MySQL' : 'SQLite' }})
                </option>
              </select>
            </div>
            
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
                  @click="activeMenu = 'metadata'"
                  class="w-full text-left px-3 py-2 rounded-lg transition-colors flex items-center gap-2"
                  :class="activeMenu === 'metadata' ? 'bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400' : 'text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-800'"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                  </svg>
                  元数据管理
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
          
          <!-- 元数据管理 -->
          <div v-else-if="activeMenu === 'metadata'" class="h-full flex overflow-hidden">
            <!-- 左侧目录树 -->
            <div class="w-1/4 border-r border-gray-200 dark:border-gray-700 p-4 overflow-y-auto">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">数据源目录</h3>
              <!-- 目录树 -->
              <div class="space-y-1">
                <!-- 根节点：数据源 -->
                <div 
                  class="font-medium text-gray-900 dark:text-white mb-2 py-2 px-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 cursor-pointer flex items-center"
                  @click="toggleRoot"
                >
                  <svg class="w-4 h-4 mr-2 transition-transform" :class="rootExpanded ? 'transform rotate-90' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                  </svg>
                  数据源
                </div>
                <!-- 数据源子节点 -->
                <div v-if="rootExpanded" class="pl-4 space-y-1">
                  <template v-for="source in dataSources" :key="source.id">
                    <div 
                      class="py-2 px-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 cursor-pointer flex items-center"
                      :class="selectedDataSource?.id === source.id ? 'bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400' : ''"
                      @click="handleDataSourceClick(source)"
                    >
                      <svg class="w-4 h-4 mr-2 transition-transform" :class="expandedDataSourceId === source.id ? 'transform rotate-90' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                      </svg>
                      {{ source.name }}
                    </div>
                    <!-- 库表节点（展开的数据源下的库表） -->
                    <div v-if="expandedDataSourceId === source.id && tables.length > 0" class="pl-8 mt-1 space-y-1 border-l-2 border-gray-300 dark:border-gray-600">
                      <div 
                        v-for="table in tables" 
                        :key="table.id" 
                        class="py-2 px-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 cursor-pointer text-sm"
                        :class="selectedTable?.id === table.id ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400' : ''"
                        @click.stop="handleTableClick(table)"
                      >
                        {{ table.table_name }}
                      </div>
                    </div>
                  </template>
                  <div v-if="dataSources.length === 0" class="py-4 text-center text-gray-500 dark:text-gray-400 text-sm">
                    暂无数据源
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 右侧功能区 -->
            <div class="flex-1 p-6 overflow-y-auto">
              <!-- 数据源列表（未选择数据源时显示） -->
              <div v-if="!selectedDataSource" class="h-full">
                <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">数据源列表</h3>
                <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
                  <div class="overflow-x-auto">
                    <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                      <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                        <tr>
                          <th scope="col" class="px-6 py-3">名称</th>
                          <th scope="col" class="px-6 py-3">类型</th>
                          <th scope="col" class="px-6 py-3">状态</th>
                          <th scope="col" class="px-6 py-3">描述</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="source in dataSources" :key="source.id" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700">
                          <td class="px-6 py-4 font-medium text-gray-900 dark:text-white">{{ source.name }}</td>
                          <td class="px-6 py-4">{{ source.type === 'mysql' ? 'MySQL' : 'SQLite' }}</td>
                          <td class="px-6 py-4">
                            <span :class="{
                              'px-2 py-1 text-xs font-medium rounded-full': true,
                              'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200': source.status === 'active',
                              'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200': source.status === 'inactive'
                            }">
                              {{ source.status === 'active' ? '活跃' : '非活跃' }}
                            </span>
                          </td>
                          <td class="px-6 py-4 max-w-xs truncate" :title="source.description">{{ source.description || '-' }}</td>
                        </tr>
                        <tr v-if="dataSources.length === 0">
                          <td colspan="4" class="px-6 py-8 text-center text-gray-500 dark:text-gray-400">
                            暂无数据源
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
              
              <!-- 库表列表（选择数据源时显示） -->
              <div v-else-if="!selectedTable" class="h-full">
                <div class="flex items-center justify-between mb-4">
                  <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
                    {{ selectedDataSource.name }} 的库表
                  </h3>
                  <button 
                    class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
                    @click="handleRefreshMetadata"
                  >
                    更新元数据
                  </button>
                </div>
                <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
                  <div class="overflow-x-auto">
                    <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                      <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                        <tr>
                          <th scope="col" class="px-6 py-3">表名</th>
                          <th scope="col" class="px-6 py-3">描述</th>
                          <th scope="col" class="px-6 py-3">操作</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="table in tables" :key="table.id" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700">
                          <td class="px-6 py-4 font-medium text-gray-900 dark:text-white">{{ table.table_name }}</td>
                          <td class="px-6 py-4 max-w-xs truncate" :title="table.table_description">{{ table.table_description || '-' }}</td>
                          <td class="px-6 py-4">
                            <button class="text-blue-600 dark:text-blue-400 hover:underline mr-4">查看</button>
                            <button class="text-green-600 dark:text-green-400 hover:underline">编辑</button>
                          </td>
                        </tr>
                        <tr v-if="tables.length === 0">
                          <td colspan="3" class="px-6 py-8 text-center text-gray-500 dark:text-gray-400">
                            暂无库表
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
              
              <!-- 库表结构（选择库表时显示） -->
              <div v-else class="h-full">
                <div class="flex items-center justify-between mb-4">
                  <div class="flex items-center space-x-4">
                    <button 
                      class="px-3 py-1 text-sm bg-gray-200 dark:bg-gray-700 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
                      @click="selectedTable = null"
                    >
                      ← 返回
                    </button>
                    <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
                      {{ selectedTable.table_name }} - 表结构
                    </h3>
                  </div>
                </div>
                
                <!-- 字段信息 -->
                <div class="mb-6">
                  <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">字段信息</h4>
                  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
                    <div class="overflow-x-auto">
                      <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                        <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                          <tr>
                            <th scope="col" class="px-4 py-3">字段名</th>
                            <th scope="col" class="px-4 py-3">类型</th>
                            <th scope="col" class="px-4 py-3">描述</th>
                            <th scope="col" class="px-4 py-3">键</th>
                            <th scope="col" class="px-4 py-3">可空</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="col in tableStructure?.columns" :key="col.name" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700">
                            <td class="px-4 py-3 font-medium text-gray-900 dark:text-white">{{ col.name }}</td>
                            <td class="px-4 py-3 font-mono text-xs">{{ col.type }}</td>
                            <td class="px-4 py-3">{{ col.description }}</td>
                            <td class="px-4 py-3">{{ col.key || '-' }}</td>
                            <td class="px-4 py-3">{{ col.nullable ? '是' : '否' }}</td>
                          </tr>
                          <tr v-if="!tableStructure?.columns || tableStructure.columns.length === 0">
                            <td colspan="5" class="px-6 py-8 text-center text-gray-500 dark:text-gray-400">
                              暂无字段信息
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
                
                <!-- 索引信息 -->
                <div>
                  <h4 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">索引信息</h4>
                  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
                    <div class="overflow-x-auto">
                      <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                        <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                          <tr>
                            <th scope="col" class="px-4 py-3">索引名</th>
                            <th scope="col" class="px-4 py-3">列</th>
                            <th scope="col" class="px-4 py-3">类型</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="idx in tableStructure?.indexes" :key="idx.name" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700">
                            <td class="px-4 py-3 font-medium text-gray-900 dark:text-white">{{ idx.name }}</td>
                            <td class="px-4 py-3 font-mono text-xs">{{ idx.columns.join(', ') }}</td>
                            <td class="px-4 py-3 font-mono text-xs">{{ idx.type }}</td>
                          </tr>
                          <tr v-if="!tableStructure?.indexes || tableStructure.indexes.length === 0">
                            <td colspan="3" class="px-6 py-8 text-center text-gray-500 dark:text-gray-400">
                              暂无索引信息
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              </div>
            </div>
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
import api from '@/services/api'

const chatStore = useChatStore()
const inputText = ref('')
const messagesContainer = ref(null)
const isDark = ref(false)
const isAdminPage = ref(false)
const activeMenu = ref('knowledge-base')
const dataSources = ref([])
const selectedDataSource = ref(null)
const tables = ref([])
const expandedDataSourceId = ref(null)
const selectedTable = ref(null)
const tableStructure = ref(null)
const rootExpanded = ref(true)

// 对话界面数据源选择
const selectedDataSourceId = ref('')

// 加载数据源列表（对话界面用）
const loadDataSourceList = async () => {
  try {
    const response = await api.getDataSources()
    if (response.type === 'data_sources') {
      dataSources.value = response.data
      
      // 优先使用上次选中的数据源
      if (selectedDataSourceId.value) {
        const source = dataSources.value.find(s => s.id === parseInt(selectedDataSourceId.value))
        if (source) {
          selectedDataSource.value = source
          return
        }
      }
      
      // 如果没有上次选择，自动选择默认数据源
      const defaultSource = dataSources.value.find(s => s.is_default)
      if (defaultSource) {
        selectedDataSourceId.value = defaultSource.id.toString()
        selectedDataSource.value = defaultSource
        console.log('自动选择默认数据源:', defaultSource.name)
      }
    }
  } catch (error) {
    console.error('Error loading data sources:', error)
  }
}

// 处理数据源选择变化
const handleDataSourceChange = () => {
  if (selectedDataSourceId.value) {
    const source = dataSources.value.find(s => s.id === parseInt(selectedDataSourceId.value))
    selectedDataSource.value = source
    if (source) {
      console.log('已选择数据源:', source.name)
      // 这里可以添加通知后端或其他处理逻辑
    }
  } else {
    selectedDataSource.value = null
  }
}

// 加载数据源列表
const loadDataSources = async () => {
  try {
    const response = await api.getDataSources()
    if (response.type === 'data_sources') {
      dataSources.value = response.data
    }
  } catch (error) {
    console.error('Error loading data sources:', error)
  }
}

// 监听菜单切换，当切换到元数据管理时加载数据源
watch(activeMenu, (newMenu) => {
  if (newMenu === 'metadata') {
    loadDataSources()
  }
})

// 处理根节点点击事件
const handleRootNodeClick = () => {
  // 点击根节点时重新加载数据源列表
  loadDataSources()
  selectedDataSource.value = null
  tables.value = []
  expandedDataSourceId.value = null
}

// 切换根节点展开/收起状态
const toggleRoot = () => {
  rootExpanded.value = !rootExpanded.value
  if (!rootExpanded.value) {
    // 收起时清空选中的项
    selectedDataSource.value = null
    tables.value = []
    expandedDataSourceId.value = null
  } else {
    // 展开时重新加载数据源
    loadDataSources()
  }
}

// 处理数据源子节点点击事件
const handleDataSourceClick = (source) => {
  // 切换展开/收起状态
  if (expandedDataSourceId.value === source.id) {
    // 当前是展开状态，点击后收起
    expandedDataSourceId.value = null
  } else {
    // 当前是收起状态，点击后展开
    // 先清空库表数据和选中的库表，避免显示上一个数据源的库表
    tables.value = []
    selectedTable.value = null
    tableStructure.value = null
    selectedDataSource.value = source
    loadTables(source.id)
    expandedDataSourceId.value = source.id
  }
}

// 处理库表节点点击事件
const handleTableClick = (table) => {
  selectedTable.value = table
  loadTableStructure(table.id)
}

// 处理更新元数据
const handleRefreshMetadata = async () => {
  if (!selectedDataSource.value) {
    alert('请先选择一个数据源')
    return
  }
  
  try {
    const response = await api.refreshMetadata(selectedDataSource.value.id)
    if (response.type === 'success') {
      alert(response.message)
      // 重新加载库表列表
      await loadTables(selectedDataSource.value.id)
    } else {
      alert('更新元数据失败：' + response.error)
    }
  } catch (error) {
    console.error('Error refreshing metadata:', error)
    alert('更新元数据失败：' + error.message)
  }
}

// 加载库表结构
const loadTableStructure = async (tableId) => {
  try {
    // 调用 API 获取库表结构
    const response = await api.getTableStructure(tableId)
    if (response.type === 'table_structure') {
      tableStructure.value = response.data
    } else {
      console.error('Failed to load table structure:', response)
      tableStructure.value = null
    }
  } catch (error) {
    console.error('Error loading table structure:', error)
    tableStructure.value = null
  }
}

// 加载数据源的库表列表
const loadTables = async (dataSourceId) => {
  try {
    // 调用API获取库表列表
    const response = await api.getDataSourceTables(dataSourceId)
    if (response.type === 'tables') {
      tables.value = response.data
    }
  } catch (error) {
    console.error('Error loading tables:', error)
    tables.value = []
  }
}

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
  
  // Load data sources for selection
  loadDataSourceList()
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
