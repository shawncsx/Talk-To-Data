<template>
  <div class="space-y-6">
    <!-- 数据源列表 -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">数据源列表</h3>
        <button 
          @click="showAddModal = true"
          class="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
          添加数据源
        </button>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                名称
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                类型
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                连接信息
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                状态
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                操作
              </th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="source in dataSources" :key="source.id">
              <td class="px-6 py-4 whitespace-nowrap max-w-xs">
                <div class="text-sm font-medium text-gray-900 dark:text-white truncate" :title="source.name">{{ source.name }}</div>
                <div v-if="source.description" class="text-sm text-gray-500 dark:text-gray-400 truncate" :title="source.description">{{ source.description }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="source.type === 'mysql' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200' : 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'">
                  {{ source.type.toUpperCase() }}
                </span>
              </td>
              <td class="px-6 py-4 max-w-xs">
                <div class="text-sm text-gray-900 dark:text-white truncate" :title="source.type === 'mysql' ? `${source.mysql_host}:${source.mysql_port}/${source.mysql_database}` : source.sqlite_path">
                  <template v-if="source.type === 'mysql'">
                    {{ source.mysql_host }}:{{ source.mysql_port }}/{{ source.mysql_database }}
                  </template>
                  <template v-else>
                    {{ source.sqlite_path }}
                  </template>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="source.status === 'active' ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'">
                  {{ source.status }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button 
                  @click="editDataSource(source)"
                  class="text-primary-600 hover:text-primary-900 dark:text-primary-400 dark:hover:text-primary-300 mr-3"
                >
                  编辑
                </button>
                <button 
                  @click="deleteDataSource(source)"
                  class="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300"
                  :disabled="source.id === 1"
                >
                  删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="dataSources.length === 0" class="px-6 py-12 text-center">
        <div class="text-gray-400">暂无数据源</div>
      </div>
    </div>

    <!-- 添加/编辑数据源模态框 -->
    <div v-if="showAddModal || showEditModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-hidden flex flex-col">
        <!-- 模态框头部 -->
        <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
            {{ showEditModal ? '编辑数据源' : '添加数据源' }}
          </h3>
          <button
            @click="closeModal"
            class="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <!-- 模态框内容 -->
        <div class="flex-1 overflow-y-auto p-6">
          <form @submit.prevent="saveDataSource" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                数据源名称 *
              </label>
              <input 
                v-model="formData.name" 
                type="text" 
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
                required
              >
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                数据源类型 *
              </label>
              <select 
                v-model="formData.type" 
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
                required
              >
                <option value="mysql">MySQL</option>
                <option value="sqlite">SQLite</option>
              </select>
            </div>

            <!-- MySQL 特定字段 -->
            <div v-if="formData.type === 'mysql'" class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  主机地址 *
                </label>
                <input 
                  v-model="formData.mysql_host" 
                  type="text" 
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
                  required
                >
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  端口
                </label>
                <input 
                  v-model="formData.mysql_port" 
                  type="number" 
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
                >
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  数据库名称 *
                </label>
                <input 
                  v-model="formData.mysql_database" 
                  type="text" 
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
                  required
                >
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  用户名 *
                </label>
                <input 
                  v-model="formData.mysql_username" 
                  type="text" 
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
                  required
                >
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  密码
                </label>
                <input 
                  v-model="formData.mysql_password" 
                  type="password" 
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
                >
              </div>
            </div>

            <!-- SQLite 特定字段 -->
            <div v-else-if="formData.type === 'sqlite'">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  数据库文件路径 *
                </label>
                <input 
                  v-model="formData.sqlite_path" 
                  type="text" 
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
                  required
                >
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                描述
              </label>
              <textarea 
                v-model="formData.description" 
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
                rows="3"
              ></textarea>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                状态
              </label>
              <select 
                v-model="formData.status" 
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:text-white"
              >
                <option value="active">活跃</option>
                <option value="inactive">非活跃</option>
              </select>
            </div>

            <div class="pt-4">
              <button 
                @click="testConnection"
                type="button"
                class="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition-colors mr-2"
              >
                测试连接
              </button>
              <button 
                type="submit"
                class="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors"
              >
                {{ showEditModal ? '保存修改' : '添加数据源' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- 确认删除模态框 -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-xl max-w-md w-full">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">确认删除</h3>
        </div>
        <div class="px-6 py-4">
          <p class="text-gray-700 dark:text-gray-300">
            确定要删除数据源 "{{ deleteSource?.name }}" 吗？此操作无法撤销。
          </p>
        </div>
        <div class="px-6 py-4 border-t border-gray-200 dark:border-gray-700 flex justify-end gap-2">
          <button 
            @click="showDeleteModal = false"
            class="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 dark:bg-gray-700 dark:hover:bg-gray-600 dark:text-gray-200 rounded-lg transition-colors"
          >
            取消
          </button>
          <button 
            @click="confirmDelete"
            class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
          >
            删除
          </button>
        </div>
      </div>
    </div>

    <!-- 通知消息 -->
    <div v-if="notification" class="fixed bottom-4 right-4 z-50 max-w-md" :class="notification.type === 'success' ? 'bg-green-500' : 'bg-red-500'">
      <div class="p-4 rounded-lg shadow-lg text-white">
        <div class="flex items-center gap-2">
          <svg v-if="notification.type === 'success'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-.77-2.694-.77-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
          </svg>
          <span>{{ notification.message }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

// 响应式数据
const dataSources = ref([])
const showAddModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const formData = ref({})
const deleteSource = ref(null)
const notification = ref(null)

// 加载数据源列表
const loadDataSources = async () => {
  try {
    const response = await api.getDataSources()
    if (response.type === 'data_sources') {
      dataSources.value = response.data
    }
  } catch (error) {
    showNotification('error', '加载数据源失败')
    console.error('Error loading data sources:', error)
  }
}

// 打开添加模态框
const openAddModal = () => {
  formData.value = {
    name: '',
    type: 'mysql',
    mysql_port: 3306,
    status: 'active'
  }
  showAddModal.value = true
  showEditModal.value = false
}

// 打开编辑模态框
const editDataSource = (source) => {
  formData.value = { ...source }
  showEditModal.value = true
  showAddModal.value = false
}

// 关闭模态框
const closeModal = () => {
  showAddModal.value = false
  showEditModal.value = false
  showDeleteModal.value = false
  formData.value = {}
  deleteSource.value = null
}

// 保存数据源
const saveDataSource = async () => {
  try {
    let response
    if (showEditModal.value) {
      response = await api.updateDataSource(formData.value.id, formData.value)
    } else {
      response = await api.addDataSource(formData.value)
    }
    
    if (response.type === 'success') {
      showNotification('success', showEditModal.value ? '数据源更新成功' : '数据源添加成功')
      closeModal()
      loadDataSources()
    }
  } catch (error) {
    showNotification('error', '保存数据源失败')
    console.error('Error saving data source:', error)
  }
}

// 测试连接
const testConnection = async () => {
  try {
    const response = await api.testDataSource(formData.value)
    if (response.type === 'success') {
      showNotification('success', '连接测试成功')
    } else {
      showNotification('error', response.error || '连接测试失败')
    }
  } catch (error) {
    showNotification('error', '连接测试失败')
    console.error('Error testing connection:', error)
  }
}

// 打开删除确认模态框
const deleteDataSource = (source) => {
  deleteSource.value = source
  showDeleteModal.value = true
}

// 确认删除
const confirmDelete = async () => {
  if (!deleteSource.value) return
  
  try {
    const response = await api.deleteDataSource(deleteSource.value.id)
    if (response.type === 'success') {
      showNotification('success', '数据源删除成功')
      closeModal()
      loadDataSources()
    }
  } catch (error) {
    showNotification('error', '删除数据源失败')
    console.error('Error deleting data source:', error)
  }
}

// 显示通知
const showNotification = (type, message) => {
  notification.value = { type, message }
  setTimeout(() => {
    notification.value = null
  }, 3000)
}

// 初始化
onMounted(() => {
  loadDataSources()
})
</script>

<style scoped>
/* 自定义样式 */
</style>