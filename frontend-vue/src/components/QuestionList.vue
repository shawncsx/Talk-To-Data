<template>
  <div class="question-list">
    <h3 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3 uppercase tracking-wider">
      {{ title }}
    </h3>
    <div class="space-y-2">
      <button
        v-for="(question, index) in questions"
        :key="index"
        @click="$emit('select', question)"
        class="w-full text-left p-3 rounded-lg bg-gray-50 dark:bg-gray-800 hover:bg-primary-50 dark:hover:bg-primary-900/20 border border-gray-200 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-700 transition-all group"
        :disabled="disabled"
      >
        <p class="text-sm text-gray-700 dark:text-gray-300 group-hover:text-primary-700 dark:group-hover:text-primary-400 line-clamp-2">
          {{ question }}
        </p>
      </button>
    </div>
    <div v-if="questions.length === 0" class="text-center py-4 text-gray-500 text-sm">
      暂无问题
    </div>
  </div>
</template>

<script setup>
defineProps({
  questions: {
    type: Array,
    default: () => []
  },
  title: {
    type: String,
    default: '推荐问题'
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

defineEmits(['select'])
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
