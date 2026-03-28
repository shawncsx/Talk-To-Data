<template>
  <div class="chart-display">
    <div class="flex items-center justify-between mb-3">
      <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200">数据可视化</h3>
    </div>
    <div ref="chartContainer" class="w-full bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import Plotly from 'plotly.js-dist-min'

const props = defineProps({
  chartData: {
    type: String,
    required: true
  }
})

const chartContainer = ref(null)
let chartInstance = null

onMounted(() => {
  renderChart()
})

onUnmounted(() => {
  if (chartContainer.value) {
    Plotly.purge(chartContainer.value)
  }
})

watch(() => props.chartData, () => {
  renderChart()
}, { deep: true })

function renderChart() {
  if (!chartContainer.value || !props.chartData) return
  
  try {
    const figure = JSON.parse(props.chartData)
    
    // 设置图表容器高度
    const layout = {
      ...figure.layout,
      autosize: true,
      height: 400,
      paper_bgcolor: 'transparent',
      plot_bgcolor: 'transparent',
      font: {
        color: document.documentElement.classList.contains('dark') ? '#e5e7eb' : '#374151'
      }
    }
    
    const config = {
      responsive: true,
      displayModeBar: true,
      displaylogo: false,
      modeBarButtonsToRemove: ['lasso2d', 'select2d']
    }
    
    Plotly.newPlot(chartContainer.value, figure.data, layout, config)
    
    // 监听主题变化
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.attributeName === 'class') {
          const isDark = document.documentElement.classList.contains('dark')
          Plotly.relayout(chartContainer.value, {
            'font.color': isDark ? '#e5e7eb' : '#374151'
          })
        }
      })
    })
    
    observer.observe(document.documentElement, { attributes: true })
    
  } catch (err) {
    console.error('图表渲染失败:', err)
    chartContainer.value.innerHTML = '<div class="p-4 text-red-500">图表渲染失败</div>'
  }
}
</script>

<style scoped>
.chart-display {
  @apply w-full;
}
</style>
