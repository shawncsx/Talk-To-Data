<template>
  <div class="sql-display bg-gray-900 rounded-lg overflow-hidden">
    <div class="flex items-center justify-between px-4 py-2 bg-gray-800 border-b border-gray-700">
      <span class="text-gray-300 text-sm font-medium">生成的 SQL</span>
      <button 
        @click="copySql"
        class="text-gray-400 hover:text-white transition-colors text-sm flex items-center gap-1"
      >
        <svg v-if="!copied" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
        </svg>
        <svg v-else class="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
        </svg>
        {{ copied ? '已复制' : '复制' }}
      </button>
    </div>
    <pre class="p-4 overflow-x-auto whitespace-pre-wrap break-all"><code ref="codeRef" class="sql-syntax text-sm text-blue-300">{{ formattedSql }}</code></pre>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import hljs from 'highlight.js/lib/core'
import sql from 'highlight.js/lib/languages/sql'

hljs.registerLanguage('sql', sql)

const props = defineProps({
  sql: {
    type: String,
    required: true
  }
})

const codeRef = ref(null)
const copied = ref(false)

// 简单的 SQL 格式化函数
const formattedSql = computed(() => {
  return formatSql(props.sql)
})

// SQL 格式化函数
function formatSql(sql) {
  if (!sql) return ''
  
  // 清理输入
  let formatted = sql.trim()
  
  // 关键字列表（大写）
  const keywords = [
    'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'NOT', 'IN', 'EXISTS',
    'JOIN', 'INNER', 'LEFT', 'RIGHT', 'FULL', 'OUTER', 'ON',
    'GROUP', 'BY', 'ORDER', 'HAVING', 'LIMIT', 'OFFSET',
    'INSERT', 'INTO', 'VALUES', 'UPDATE', 'SET', 'DELETE',
    'CREATE', 'TABLE', 'ALTER', 'DROP', 'INDEX', 'VIEW',
    'UNION', 'ALL', 'DISTINCT', 'AS', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END',
    'COUNT', 'SUM', 'AVG', 'MAX', 'MIN', 'ASC', 'DESC'
  ]
  
  // 1. 规范化空格
  formatted = formatted.replace(/\s+/g, ' ')
  
  // 2. 在关键字前添加换行（除了 SELECT）
  keywords.forEach(keyword => {
    const regex = new RegExp(`\\b${keyword}\\b`, 'gi')
    if (keyword !== 'SELECT') {
      formatted = formatted.replace(regex, '\n' + keyword)
    } else {
      formatted = formatted.replace(regex, keyword)
    }
  })
  
  // 3. 处理逗号后的换行
  formatted = formatted.replace(/,\s*/g, ',\n    ')
  
  // 4. 处理 SELECT 后的字段缩进
  formatted = formatted.replace(/SELECT\s+/i, 'SELECT\n    ')
  
  // 5. 处理 FROM、WHERE 等关键字后的内容
  formatted = formatted.replace(/\n(FROM|WHERE|GROUP BY|ORDER BY|HAVING|LIMIT)\s+/gi, '\n$1\n    ')
  
  // 6. 处理 JOIN
  formatted = formatted.replace(/\n(INNER JOIN|LEFT JOIN|RIGHT JOIN|FULL JOIN|JOIN)\s+/gi, '\n$1\n    ')
  
  // 7. 处理 ON 子句
  formatted = formatted.replace(/\nON\s+/gi, '\nON ')
  
  // 8. 处理 AND 和 OR
  formatted = formatted.replace(/\n(AND|OR)\s+/gi, '\n    $1 ')
  
  // 9. 清理多余的换行和空格
  formatted = formatted.replace(/\n\s*\n/g, '\n')
  
  // 10. 确保没有前导换行
  formatted = formatted.trim()
  
  return formatted
}

// 监听 SQL 变化，重新高亮
watch(() => props.sql, () => {
  nextTick(() => {
    if (codeRef.value) {
      hljs.highlightElement(codeRef.value)
    }
  })
}, { immediate: true })

onMounted(() => {
  if (codeRef.value) {
    hljs.highlightElement(codeRef.value)
  }
})

async function copySql() {
  try {
    await navigator.clipboard.writeText(props.sql)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    console.error('复制失败:', err)
  }
}
</script>

<style scoped>
.sql-display {
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
}

pre {
  margin: 0;
}

pre code {
  display: block;
  white-space: pre-wrap;
  word-break: break-all;
  overflow-wrap: break-word;
  line-height: 1.5;
}

code {
  font-family: inherit;
}
</style>
