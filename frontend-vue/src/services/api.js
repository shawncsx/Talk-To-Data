import axios from 'axios'

const API_BASE_URL = '/api/v0'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const api = {
  // 获取示例问题列表
  async generateQuestions() {
    const response = await apiClient.get('/generate_questions')
    return response.data
  },

  // 自然语言转 SQL
  async generateSql(question) {
    const response = await apiClient.get('/generate_sql', {
      params: { question }
    })
    return response.data
  },

  // 执行 SQL 查询
  async runSql(id) {
    const response = await apiClient.get('/run_sql', {
      params: { id }
    })
    return response.data
  },

  // 下载 CSV
  downloadCsv(id) {
    window.open(`${API_BASE_URL}/download_csv?id=${id}`, '_blank')
  },

  // 生成可视化图表
  async generatePlotlyFigure(id) {
    const response = await apiClient.get('/generate_plotly_figure', {
      params: { id }
    })
    return response.data
  },

  // 获取训练数据
  async getTrainingData() {
    const response = await apiClient.get('/get_training_data')
    return response.data
  },

  // 删除训练数据
  async removeTrainingData(id) {
    const response = await apiClient.post('/remove_training_data', { id })
    return response.data
  },

  // 添加训练数据
  async train(data) {
    const response = await apiClient.post('/train', data)
    return response.data
  },

  // 生成跟进问题
  async generateFollowupQuestions(id) {
    const response = await apiClient.get('/generate_followup_questions', {
      params: { id }
    })
    return response.data
  },

  // 加载历史问题
  async loadQuestion(id) {
    const response = await apiClient.get('/load_question', {
      params: { id }
    })
    return response.data
  },

  // 获取问题历史
  async getQuestionHistory() {
    const response = await apiClient.get('/get_question_history')
    return response.data
  }
}

export default api
