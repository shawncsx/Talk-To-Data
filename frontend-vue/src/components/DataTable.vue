<template>
  <div class="data-table-container">
    <div class="flex items-center justify-between mb-3">
      <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200">
        查询结果
        <span class="text-sm font-normal text-gray-500 ml-2">({{ rowCount }} 行)</span>
      </h3>
      <button 
        @click="downloadCsv"
        class="px-3 py-1.5 bg-primary-600 hover:bg-primary-700 text-white text-sm rounded-lg transition-colors flex items-center gap-2"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
        </svg>
        下载 CSV
      </button>
    </div>
    
    <div class="overflow-x-auto border border-gray-200 dark:border-gray-700 rounded-lg">
      <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead class="bg-gray-50 dark:bg-gray-800">
          <tr>
            <th 
              v-for="column in columns" 
              :key="column"
              class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
            >
              {{ column }}
            </th>
          </tr>
        </thead>
        <tbody class="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
          <tr 
            v-for="(row, index) in data" 
            :key="index"
            class="hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
          >
            <td 
              v-for="column in columns" 
              :key="column"
              class="px-4 py-3 text-sm text-gray-900 dark:text-gray-300 whitespace-nowrap"
            >
              {{ formatValue(row[column]) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    required: true
  },
  id: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['download'])

const columns = computed(() => {
  if (!props.data || props.data.length === 0) return []
  return Object.keys(props.data[0])
})

const rowCount = computed(() => props.data?.length || 0)

function formatValue(value) {
  if (value === null || value === undefined) return '-'
  if (typeof value === 'number') {
    // 格式化数字，保留合适的小数位
    return Number.isInteger(value) ? value : value.toFixed(2)
  }
  return value
}

function downloadCsv() {
  emit('download')
}
</script>

<style scoped>
.data-table-container {
  @apply w-full;
}
</style>
