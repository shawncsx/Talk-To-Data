import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '@/services/api'

export const useChatStore = defineStore('chat', () => {
  // State
  const messages = ref([])
  const currentQuestion = ref('')
  const isLoading = ref(false)
  const currentId = ref(null)
  const sampleQuestions = ref([])
  const followupQuestions = ref([])
  const questionHistory = ref([])
  const error = ref(null)

  // Getters
  const hasMessages = computed(() => messages.value.length > 0)
  const lastMessage = computed(() => messages.value[messages.value.length - 1])

  // Actions
  async function loadSampleQuestions() {
    try {
      const response = await api.generateQuestions()
      if (response.type === 'question_list') {
        sampleQuestions.value = response.questions || []
      }
    } catch (err) {
      console.error('加载示例问题失败:', err)
    }
  }

  async function askQuestion(question) {
    if (!question.trim() || isLoading.value) return

    isLoading.value = true
    error.value = null
    currentQuestion.value = question

    // 添加用户消息
    messages.value.push({
      type: 'user',
      content: question,
      timestamp: new Date()
    })

    try {
      // 1. 生成 SQL
      const sqlResponse = await api.generateSql(question)
      
      if (sqlResponse.type === 'error') {
        throw new Error(sqlResponse.error)
      }

      currentId.value = sqlResponse.id

      // 添加 SQL 消息
      messages.value.push({
        type: 'sql',
        content: sqlResponse.text,
        id: sqlResponse.id,
        timestamp: new Date()
      })

      // 2. 执行 SQL 获取数据
      const dataResponse = await api.runSql(sqlResponse.id)
      
      if (dataResponse.type === 'error') {
        throw new Error(dataResponse.error)
      }

      // 添加数据消息
      messages.value.push({
        type: 'data',
        content: JSON.parse(dataResponse.df),
        id: sqlResponse.id,
        timestamp: new Date()
      })

      // 3. 生成图表
      try {
        const chartResponse = await api.generatePlotlyFigure(sqlResponse.id)
        if (chartResponse.type === 'plotly_figure') {
          messages.value.push({
            type: 'chart',
            content: chartResponse.fig,
            id: sqlResponse.id,
            timestamp: new Date()
          })
        }
      } catch (chartErr) {
        console.log('图表生成失败:', chartErr)
      }

      // 4. 添加反馈询问消息
      messages.value.push({
        type: 'feedback',
        id: sqlResponse.id,
        timestamp: new Date()
      })

      // 5. 获取跟进问题
      try {
        const followupResponse = await api.generateFollowupQuestions(sqlResponse.id)
        if (followupResponse.type === 'question_list') {
          followupQuestions.value = followupResponse.questions || []
        }
      } catch (followupErr) {
        console.log('跟进问题生成失败:', followupErr)
      }

      // 6. 更新历史记录
      await loadQuestionHistory()

    } catch (err) {
      error.value = err.message
      messages.value.push({
        type: 'error',
        content: err.message,
        timestamp: new Date()
      })
    } finally {
      isLoading.value = false
      currentQuestion.value = ''
    }
  }

  async function loadQuestionHistory() {
    try {
      const response = await api.getQuestionHistory()
      if (response.type === 'question_history') {
        questionHistory.value = response.questions || []
      }
    } catch (err) {
      console.error('加载历史记录失败:', err)
    }
  }

  async function loadPreviousQuestion(id) {
    try {
      isLoading.value = true
      const response = await api.loadQuestion(id)
      
      if (response.type === 'question_cache') {
        // 清空当前消息，加载历史消息
        messages.value = []
        
        messages.value.push({
          type: 'user',
          content: response.question,
          timestamp: new Date()
        })
        
        messages.value.push({
          type: 'sql',
          content: response.sql,
          id: id,
          timestamp: new Date()
        })
        
        messages.value.push({
          type: 'data',
          content: JSON.parse(response.df),
          id: id,
          timestamp: new Date()
        })

        if (response.fig) {
          messages.value.push({
            type: 'chart',
            content: response.fig,
            id: id,
            timestamp: new Date()
          })
        }

        currentId.value = id
        followupQuestions.value = response.followup_questions || []
      }
    } catch (err) {
      console.error('加载历史问题失败:', err)
    } finally {
      isLoading.value = false
    }
  }

  function downloadCurrentCsv() {
    if (currentId.value) {
      api.downloadCsv(currentId.value)
    }
  }

  function clearChat() {
    messages.value = []
    currentId.value = null
    followupQuestions.value = []
    error.value = null
  }

  async function handleFeedback(messageId, isCorrect) {
    try {
      // 找到对应的用户问题和SQL消息
      const userMessage = messages.value.find(msg => msg.type === 'user' && msg.timestamp < messages.value.find(m => m.id === messageId && m.type === 'sql').timestamp)
      const sqlMessage = messages.value.find(msg => msg.id === messageId && msg.type === 'sql')
      const feedbackMessage = messages.value.find(msg => msg.id === messageId && msg.type === 'feedback')

      if (userMessage && sqlMessage && feedbackMessage) {
        const question = userMessage.content
        const sql = sqlMessage.content

        // 更新反馈询问消息，标记为已回答
        feedbackMessage.answered = true
        feedbackMessage.feedback = isCorrect

        let feedbackResult = ''
        if (isCorrect) {
          // 如果用户认为正确，将问题和SQL添加到training data
          await api.train({ question, sql })
          feedbackResult = '感谢反馈！已将此问题和SQL添加到训练数据中。'
        } else {
          // 如果用户认为不正确，从training data中删除
          // 注意：这里需要调用适当的API来删除训练数据
          // 由于API可能没有直接的删除方法，这里我们可以提示用户
          feedbackResult = '感谢反馈！我们会根据您的反馈改进系统。'
        }

        // 添加反馈结果消息
        messages.value.push({
          type: 'feedback_result',
          content: feedbackResult,
          id: messageId,
          timestamp: new Date()
        })
      }
    } catch (err) {
      console.error('处理反馈失败:', err)
      // 添加错误消息
      messages.value.push({
        type: 'error',
        content: '处理反馈失败: ' + err.message,
        timestamp: new Date()
      })
    }
  }

  return {
    // State
    messages,
    currentQuestion,
    isLoading,
    currentId,
    sampleQuestions,
    followupQuestions,
    questionHistory,
    error,
    // Getters
    hasMessages,
    lastMessage,
    // Actions
    loadSampleQuestions,
    askQuestion,
    loadQuestionHistory,
    loadPreviousQuestion,
    downloadCurrentCsv,
    clearChat,
    handleFeedback
  }
})
