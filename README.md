# Talk To Data

一个基于 Flask 的数据库对话系统，让您可以通过自然语言与数据库进行交互，轻松查询和分析数据。

## 项目特点

- 🤖 自然语言处理：使用先进的 AI 模型将自然语言转换为 SQL 查询
- 📊 数据可视化：自动生成查询结果的可视化图表
- 🔒 安全可靠：支持多种数据库连接方式，确保数据安全
- 🎨 直观界面：用户友好的 Web 界面，操作简单易用
- 📱 响应式设计：适配不同设备屏幕尺寸

## 技术栈

- **后端**：Flask, Python
- **前端**：HTML, CSS, JavaScript
- **AI 模型**：Vanna AI
- **数据库**：支持 Snowflake 等多种数据库

## 快速开始

### 环境要求

- Python 3.7 或更高版本
- pip 包管理器

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <your-repository-url>
   cd Talk To Data
   ```

2. **设置环境变量**
   创建 `.env` 文件并填写以下信息：
   ```
   VANNA_MODEL=
   VANNA_API_KEY=
   SNOWFLAKE_ACCOUNT=
   SNOWFLAKE_USERNAME=
   SNOWFLAKE_PASSWORD=
   SNOWFLAKE_DATABASE=
   SNOWFLAKE_WAREHOUSE=
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **运行服务器**
   ```bash
   python app.py
   ```

5. **访问应用**
   打开浏览器，访问 `http://localhost:5000`

## 使用方法

1. 在文本框中输入自然语言查询，例如："最近一个月的销售数据"
2. 系统会自动将其转换为 SQL 查询并执行
3. 查看查询结果和生成的可视化图表
4. 可以保存和导出查询结果

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

