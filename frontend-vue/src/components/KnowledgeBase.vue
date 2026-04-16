<template>
  <div class="knowledge-base h-full flex flex-col">
    <!-- 顶部标题栏 -->
    <div class="flex items-center justify-between mb-4 flex-shrink-0">
      <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200">知识库管理</h3>
      <button
        @click="showAddModal = true"
        class="px-3 py-1.5 bg-primary-600 hover:bg-primary-700 text-white text-sm rounded-lg transition-colors flex items-center gap-2"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
        </svg>
        添加知识
      </button>
    </div>

    <!-- 主体内容区 - 左右分栏 -->
    <div class="flex-1 flex gap-4 overflow-hidden min-h-0">
      <!-- 左栏：数据源目录 -->
      <div class="w-1/3 min-w-[250px] flex flex-col border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
        <div class="px-4 py-3 bg-gray-50 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
          <h4 class="text-sm font-semibold text-gray-700 dark:text-gray-300">数据源目录</h4>
        </div>
        <div class="flex-1 overflow-y-auto p-2">
          <!-- 根节点 -->
          <div class="mb-2">
            <div 
              class="flex items-center gap-2 px-3 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg cursor-pointer transition-colors"
              @click="rootExpanded = !rootExpanded"
            >
              <svg 
                class="w-4 h-4 text-gray-500 transition-transform"
                :class="{ 'transform rotate-90': rootExpanded }"
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
              </svg>
              <svg class="w-4 h-4 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 19a2 2 0 01-2-2V7a2 2 0 012-2h4l2 2h4a2 2 0 012 2v1M5 19h14a2 2 0 002-2v-5a2 2 0 00-2-2H9a2 2 0 00-2 2v5a2 2 0 01-2 2z"></path>
              </svg>
              <span class="text-sm font-medium text-gray-700 dark:text-gray-300">数据源</span>
            </div>
            
            <!-- 数据源列表 -->
            <div v-if="rootExpanded" class="ml-4 mt-2 space-y-1">
              <div 
                v-for="source in dataSources" 
                :key="source.id"
                class="flex items-center gap-2 px-3 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg cursor-pointer transition-colors"
                :class="{ 'bg-blue-50 dark:bg-blue-900/20': selectedDataSource?.id === source.id }"
                @click="handleDataSourceClick(source)"
              >
                <svg 
                  v-if="expandedDataSourceId === source.id"
                  class="w-4 h-4 text-gray-500 transition-transform transform rotate-90"
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
                <svg 
                  v-else
                  class="w-4 h-4 text-gray-500"
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
                <svg class="w-4 h-4 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"></path>
                </svg>
                <span class="text-sm text-gray-700 dark:text-gray-300 truncate">{{ source.name }}</span>
                <span v-if="source.is_default" class="ml-auto px-2 py-0.5 text-xs bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200 rounded">
                  默认
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右栏：知识库功能区 -->
      <div class="flex-1 flex flex-col border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden min-w-0">
        <div class="px-4 py-3 bg-gray-50 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
          <h4 class="text-sm font-semibold text-gray-700 dark:text-gray-300">
            {{ selectedDataSource ? `${selectedDataSource.name} - 知识库` : '请选择数据源' }}
          </h4>
        </div>
        <div class="flex-1 overflow-y-auto p-4">
          <div v-if="!selectedDataSource" class="flex items-center justify-center h-full">
            <div class="text-center text-gray-500">
              <svg class="w-16 h-16 mx-auto mb-4 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
              </svg>
              <p class="text-sm">请从左侧选择一个数据源</p>
            </div>
          </div>
          <div v-else>
            <!-- 训练数据列表 -->
            <div class="space-y-2">
              <div
                v-for="item in trainingData"
                :key="item.id"
                class="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"
              >
                <div class="flex items-start justify-between gap-2">
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center gap-2 mb-1">
                      <span
                        class="px-2 py-0.5 text-xs rounded-full"
                        :class="getTypeClass(item.training_data_type)"
                      >
                        {{ item.training_data_type }}
                      </span>
                      <span class="text-xs text-gray-500">{{ formatDate(item.created_at) }}</span>
                    </div>
                    <p v-if="item.question" class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      {{ item.question }}
                    </p>
                    <p v-if="item.content" class="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
                      {{ item.content }}
                    </p>
                    <p v-if="item.sql" class="text-xs text-gray-500 mt-1 font-mono line-clamp-1">
                      {{ item.sql }}
                    </p>
                  </div>
                  <button
                    @click="removeTrainingData(item.id)"
                    class="p-1.5 text-gray-400 hover:text-red-500 transition-colors flex-shrink-0"
                    :disabled="isLoading"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                  </button>
                </div>
              </div>
              <div v-if="trainingData.length === 0" class="text-center py-8 text-gray-500 text-sm">
                暂无训练数据
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加知识模态框 -->
    <div
      v-if="showAddModal"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
      @click.self="showAddModal = false"
    >
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-xl max-w-lg w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">添加训练数据</h3>
          
          <!-- 类型选择 -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">类型</label>
            <div class="flex gap-2">
              <button
                v-for="type in ['question_sql', 'ddl', 'documentation']"
                :key="type"
                @click="newData.type = type"
                class="px-3 py-1.5 text-sm rounded-lg border transition-colors"
                :class="newData.type === type ? 'bg-primary-600 text-white border-primary-600' : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 border-gray-300 dark:border-gray-600'"
              >
                {{ type === 'question_sql' ? '问题-SQL' : type === 'ddl' ? 'DDL' : '文档' }}
              </button>
            </div>
          </div>

          <!-- 问题-SQL 表单 -->
          <div v-if="newData.type === 'question_sql'" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">问题</label>
              <textarea
                v-model="newData.question"
                rows="2"
                class="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-sm"
                placeholder="输入自然语言问题..."
              ></textarea>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">SQL</label>
              <textarea
                v-model="newData.sql"
                rows="3"
                class="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-sm font-mono"
                placeholder="输入对应的 SQL 语句..."
              ></textarea>
            </div>
          </div>

          <!-- DDL 表单 -->
          <div v-else-if="newData.type === 'ddl'" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">DDL 语句</label>
              <textarea
                v-model="newData.ddl"
                rows="6"
                class="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-sm font-mono"
                placeholder="CREATE TABLE ..."
              ></textarea>
            </div>
          </div>

          <!-- 文档表单 -->
          <div v-else class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">文档内容</label>
              <textarea
                v-model="newData.documentation"
                rows="6"
                class="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-3 py-2 text-sm"
                placeholder="输入业务逻辑说明、表关系描述等..."
              ></textarea>
            </div>
          </div>

          <!-- 按钮 -->
          <div class="flex justify-end gap-3 mt-6">
            <button
              @click="showAddModal = false"
              class="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              取消
            </button>
            <button
              @click="addTrainingData"
              :disabled="!canSubmit || isLoading"
              class="px-4 py-2 text-sm bg-primary-600 hover:bg-primary-700 disabled:bg-gray-300 text-white rounded-lg transition-colors flex items-center gap-2"
            >
              <svg v-if="isLoading" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ isLoading ? '保存中...' : '保存' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '@/services/api'

const trainingData = ref([])
const isLoading = ref(false)
const showAddModal = ref(false)
const newData = ref({
  type: 'question_sql',
  question: '',
  sql: '',
  ddl: '',
  documentation: ''
})

// 数据源目录相关
const dataSources = ref([])
const selectedDataSource = ref(null)
const expandedDataSourceId = ref(null)
const rootExpanded = ref(true)

const canSubmit = computed(() => {
  const { type, question, sql, ddl, documentation } = newData.value
  if (type === 'question_sql') {
    return question.trim() && sql.trim()
  } else if (type === 'ddl') {
    return ddl.trim()
  } else {
    return documentation.trim()
  }
})

onMounted(() => {
  loadTrainingData()
  loadDataSources()
})

// 加载数据源列表
async function loadDataSources() {
  try {
    const response = await api.getDataSources()
    if (response.type === 'data_sources') {
      dataSources.value = response.data
    }
  } catch (err) {
    console.error('加载数据源失败:', err)
  }
}

// 处理数据源点击
function handleDataSourceClick(source) {
  if (expandedDataSourceId.value === source.id) {
    expandedDataSourceId.value = null
  } else {
    expandedDataSourceId.value = source.id
  }
  selectedDataSource.value = source
  // 加载该数据源的训练数据
  loadTrainingDataForDataSource(source.id)
}

// 加载指定数据源的训练数据
async function loadTrainingDataForDataSource(dataSourceId) {
  try {
    isLoading.value = true
    // 这里可以调用 API 获取指定数据源的训练数据
    // const response = await api.getTrainingDataByDataSource(dataSourceId)
    // if (response.type === 'df') {
    //   trainingData.value = JSON.parse(response.df)
    // }
    // 暂时使用全部训练数据
    await loadTrainingData()
  } catch (err) {
    console.error('加载训练数据失败:', err)
  } finally {
    isLoading.value = false
  }
}

async function loadTrainingData() {
  try {
    isLoading.value = true
    const response = await api.getTrainingData()
    if (response.type === 'df') {
      trainingData.value = JSON.parse(response.df)
    }
  } catch (err) {
    console.error('加载训练数据失败:', err)
  } finally {
    isLoading.value = false
  }
}

async function addTrainingData() {
  try {
    isLoading.value = true
    const { type, question, sql, ddl, documentation } = newData.value
    
    const payload = {}
    if (type === 'question_sql') {
      payload.question = question
      payload.sql = sql
    } else if (type === 'ddl') {
      payload.ddl = ddl
    } else {
      payload.documentation = documentation
    }
    
    await api.train(payload)
    
    // 重置表单
    newData.value = {
      type: 'question_sql',
      question: '',
      sql: '',
      ddl: '',
      documentation: ''
    }
    showAddModal.value = false
    
    // 重新加载数据
    await loadTrainingData()
  } catch (err) {
    console.error('添加训练数据失败:', err)
    alert('添加失败: ' + err.message)
  } finally {
    isLoading.value = false
  }
}

async function removeTrainingData(id) {
  if (!confirm('确定要删除这条训练数据吗？')) return
  
  try {
    isLoading.value = true
    await api.removeTrainingData(id)
    await loadTrainingData()
  } catch (err) {
    console.error('删除训练数据失败:', err)
    alert('删除失败: ' + err.message)
  } finally {
    isLoading.value = false
  }
}

function getTypeClass(type) {
  const classes = {
    'question_sql': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    'ddl': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    'documentation': 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200'
  }
  return classes[type] || 'bg-gray-100 text-gray-800'
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
