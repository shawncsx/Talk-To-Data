# Talk To Data - Vue 前端

基于 Vue 3 + Vite + Tailwind CSS 重构的前端应用。

## 技术栈

- **Vue 3** - 渐进式 JavaScript 框架
- **Vite** - 下一代前端构建工具
- **Pinia** - Vue 状态管理
- **Tailwind CSS** - 实用优先的 CSS 框架
- **Axios** - HTTP 客户端
- **Plotly.js** - 数据可视化
- **Highlight.js** - 代码高亮

## 项目结构

```
frontend-vue/
├── public/                 # 静态资源
├── src/
│   ├── assets/            # 资源文件
│   ├── components/        # Vue 组件
│   │   ├── ChatInput.vue      # 聊天输入
│   │   ├── ChatMessage.vue    # 聊天消息
│   │   ├── ChartDisplay.vue   # 图表展示
│   │   ├── DataTable.vue      # 数据表格
│   │   ├── QuestionList.vue   # 问题列表
│   │   └── SqlDisplay.vue     # SQL 展示
│   ├── services/
│   │   └── api.js         # API 服务
│   ├── stores/
│   │   └── chat.js        # 聊天状态管理
│   ├── App.vue            # 根组件
│   ├── main.js            # 入口文件
│   └── style.css          # 全局样式
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## 安装和运行

### 1. 安装依赖

```bash
cd frontend-vue
npm install
```

### 2. 开发模式

```bash
npm run dev
```

应用将在 http://localhost:5173 运行

### 3. 构建生产版本

```bash
npm run build
```

构建后的文件将输出到 `static-vue` 目录

### 4. 预览生产版本

```bash
npm run preview
```

## 功能特性

- ✨ 自然语言查询数据库
- 📊 自动生成 SQL 语句
- 📈 数据可视化图表
- 💾 查询结果导出 CSV
- 🌓 暗黑模式支持
- 📱 响应式设计
- 🔄 实时对话流
- 📜 历史记录管理

## API 接口

与后端 Flask API 对接：

- `GET /api/v0/generate_questions` - 获取示例问题
- `GET /api/v0/generate_sql` - 生成 SQL
- `GET /api/v0/run_sql` - 执行 SQL
- `GET /api/v0/generate_plotly_figure` - 生成图表
- `GET /api/v0/download_csv` - 下载 CSV
- `GET /api/v0/get_question_history` - 获取历史记录

## 开发说明

### 代理配置

在 `vite.config.js` 中已配置代理，开发时自动转发 API 请求到后端：

```javascript
proxy: {
  '/api': {
    target: 'http://localhost:5000',
    changeOrigin: true
  }
}
```

### 主题切换

支持亮色/暗色主题，自动检测系统偏好。

### 组件通信

使用 Pinia 进行状态管理，组件间通过 Store 共享数据。
