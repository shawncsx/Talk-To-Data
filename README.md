# Talk To Data - 智能数据库对话系统

一个基于 Flask + Vue 3 的数据库对话系统，让您可以通过自然语言与数据库进行交互，轻松查询和分析数据。系统使用先进的大语言模型（LLM）将自然语言转换为 SQL 查询，并自动展示查询结果和可视化图表。

## 📋 目录

- [项目特点](#-项目特点)
- [系统架构](#-系统架构)
- [技术栈](#-技术栈)
- [功能模块](#-功能模块)
- [项目结构](#-项目结构)
- [数据库设计](#-数据库设计)
- [API 接口](#-api-接口)
- [前端组件](#-前端组件)
- [配置说明](#-配置说明)
- [快速开始](#-快速开始)
- [使用指南](#-使用指南)
- [开发计划](#-开发计划)

## ✨ 项目特点

- 🤖 **自然语言处理**：使用阿里云通义千问大模型将自然语言转换为 SQL 查询
- 📊 **数据可视化**：自动生成查询结果的可视化图表，支持多种图表类型
- � **多数据源支持**：支持 MySQL 和 SQLite 数据库，可动态添加/切换数据源
- 🗂️ **元数据管理**：自动管理数据库表结构、字段信息、DDL 语句
- 🧠 **向量数据库**：使用 ChromaDB 存储训练样本，提升查询准确率
- �🔒 **安全可靠**：支持数据库连接测试，确保连接安全性
- 🎨 **现代化界面**：Vue 3 + Tailwind CSS 构建响应式用户界面
- 🌙 **深色模式**：支持深色/浅色主题切换
- 📱 **响应式设计**：适配桌面和移动设备

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                        用户界面层                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │           Vue 3 前端 (App.vue)                       │    │
│  │  - 对话界面    - 后台管理    - 数据源管理            │    │
│  │  - 元数据管理  - 知识库管理  - 用户管理              │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        API 服务层                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Flask 后端 (app.py)                     │    │
│  │  - 聊天 API     - 数据源 API   - 元数据 API          │    │
│  │  - 训练 API     - 测试连接 API - 刷新元数据 API      │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        核心服务层                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Vanna AI    │  │  MySQL 服务  │  │  SQLite 服务 │      │
│  │  (LLM+RAG)   │  │              │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │  ChromaDB    │  │   缓存服务   │                         │
│  │  (向量数据库) │  │  (Memory)    │                         │
│  └──────────────┘  └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        数据存储层                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   MySQL DB   │  │  SQLite DB   │  │  ChromaDB    │      │
│  │  (元数据)    │  │  (业务数据)  │  │  (向量数据)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ 技术栈

### 后端技术
- **Web 框架**: Flask 2.x
- **AI 框架**: Vanna AI (RAG + LLM)
- **数据库驱动**: 
  - mysql-connector-python (MySQL)
  - sqlite3 (SQLite)
- **向量数据库**: ChromaDB
- **大模型**: 阿里云通义千问 (Qwen)
- **缓存**: MemoryCache (内存缓存)

### 前端技术
- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite 5.x
- **样式**: Tailwind CSS 3.x
- **状态管理**: Pinia
- **HTTP 客户端**: Axios
- **图表库**: Plotly.js

### 数据库
- **MySQL 8.0**: 存储元数据、数据源配置、用户数据
- **SQLite**: 示例数据库、业务数据
- **ChromaDB**: 向量数据库，存储训练样本

## 📦 功能模块

### 1. 对话界面（核心功能）

#### 功能描述
用户可以通过自然语言提问，系统自动转换为 SQL 查询并返回结果。

#### 主要特性
- **数据源选择**: 左侧边栏顶部提供数据源选择器，自动选择默认数据源
- **示例问题**: 提供预设问题，帮助用户快速上手
- **智能回复**: 支持文本、表格、图表等多种回复格式
- **SQL 展示**: 显示生成的 SQL 语句，支持复制
- **结果可视化**: 自动选择合适的数据可视化方式
- **历史记录**: 保存对话历史，支持查看
- **追问功能**: 基于上下文进行多轮对话

#### 界面布局
```
┌──────────────────────────────────────────────────────┐
│  左侧边栏 (固定)           │  主对话区域 (可滚动)     │
│  ┌────────────────────┐   │  ┌───────────────────┐  │
│  │ 选择数据源         │   │  │  对话消息列表     │  │
│  ├────────────────────┤   │  │  - 用户问题       │  │
│  │ 示例问题           │   │  │  - AI 回复         │  │
│  ├────────────────────┤   │  │  - 表格/图表      │  │
│  │ 历史对话           │   │  └───────────────────┘  │
│  └────────────────────┘   │  ┌───────────────────┐  │
│                           │  │  输入框           │  │
│                           │  └───────────────────┘  │
└──────────────────────────────────────────────────────┘
```

### 2. 后台管理系统

#### 2.1 数据源管理

**功能描述**
管理多个数据库连接，支持 MySQL 和 SQLite 数据源。

**主要功能**
- ✅ **数据源列表**: 展示所有已配置的数据源
- ✅ **添加数据源**: 
  - MySQL: 主机、端口、数据库名、用户名、密码
  - SQLite: 数据库文件路径
  - 自动创建向量数据库目录
- ✅ **编辑数据源**: 修改现有数据源配置
- ✅ **删除数据源**: 删除不再使用的数据源
- ✅ **测试连接**: 验证数据库连接是否可用
- ✅ **默认数据源**: 
  - 支持设置一个数据源为默认
  - 自动保证至少有一个默认数据源
  - 对话界面自动选中默认数据源
- ✅ **状态管理**: 活跃/非活跃状态切换

**数据源字段**
```sql
- id: 主键
- name: 数据源名称
- type: 类型 (mysql/sqlite)
- connection_string: 连接字符串
- mysql_host: MySQL 主机地址
- mysql_port: MySQL 端口
- mysql_database: MySQL 数据库名
- mysql_username: MySQL 用户名
- mysql_password: MySQL 密码
- sqlite_path: SQLite 文件路径
- vector_db_path: 向量数据库目录
- is_default: 是否为默认数据源
- description: 描述信息
- status: 状态 (active/inactive)
- created_at: 创建时间
- updated_at: 更新时间
```

#### 2.2 元数据管理

**功能描述**
管理数据源的元数据信息，包括表结构、字段信息、DDL 语句等。

**主要功能**
- ✅ **数据源目录树**: 
  - 根节点：数据源
  - 一级节点：各个数据源
  - 二级节点：数据源包含的库表
- ✅ **展开/收起**: 支持节点展开和收起操作
- ✅ **库表列表**: 显示选中数据源的所有表
- ✅ **表结构详情**: 
  - 字段信息（名称、类型、描述、是否主键、是否可空）
  - 索引信息
  - DDL 语句
- ✅ **更新元数据**: 从数据库重新获取最新元数据
  - MySQL: 使用 SHOW TABLES, SHOW FULL COLUMNS, SHOW CREATE TABLE
  - SQLite: 使用 sqlite_master, PRAGMA table_info

**元数据表结构**
```sql
-- metadata_tables: 存储表信息
- id: 主键
- data_source_id: 数据源 ID
- table_name: 表名
- table_ddl: 建表语句
- created_at: 创建时间
- updated_at: 更新时间

-- metadata_columns: 存储列信息
- id: 主键
- table_id: 表 ID (外键)
- column_name: 列名
- data_type: 数据类型
- column_description: 列描述
- is_primary_key: 是否主键
- is_nullable: 是否可空
- created_at: 创建时间
- updated_at: 更新时间
```

#### 2.3 知识库管理
- ⏳ 训练样本管理（待开发）
- ⏳ 问题 -SQL 对管理（待开发）
- ⏳ 业务知识库（待开发）

#### 2.4 用户管理
- ⏳ 用户列表（待开发）
- ⏳ 角色权限（待开发）
- ⏳ 操作日志（待开发）

## 📁 项目结构

```
Talk-To-Data/
├── app.py                          # Flask 后端主程序
├── cache.py                        # 内存缓存实现
├── talktodata.conf                 # 配置文件
├── talktodata.sql                  # 数据库表结构
├── requirements.txt                # Python 依赖
├── README.md                       # 项目文档
│
├── frontend-vue/                   # Vue 3 前端项目
│   ├── src/
│   │   ├── App.vue                # 主应用组件
│   │   ├── main.js                # 入口文件
│   │   ├── style.css              # 全局样式
│   │   ├── components/            # 组件目录
│   │   │   ├── ChatMessage.vue    # 聊天消息组件
│   │   │   ├── ChatInput.vue      # 输入框组件
│   │   │   ├── QuestionList.vue   # 问题列表组件
│   │   │   ├── DataSourceManager.vue  # 数据源管理组件
│   │   │   ├── KnowledgeBase.vue  # 知识库组件
│   │   │   ├── DataTable.vue      # 数据表格组件
│   │   │   ├── ChartDisplay.vue   # 图表展示组件
│   │   │   └── SqlDisplay.vue     # SQL 展示组件
│   │   ├── services/
│   │   │   └── api.js             # API 服务
│   │   └── stores/
│   │       └── chat.js            # 聊天状态管理
│   ├── package.json               # 前端依赖配置
│   ├── vite.config.js             # Vite 配置
│   └── tailwind.config.js         # Tailwind 配置
│
├── vanna/                          # Vanna AI 框架
│   └── src/vanna/                 # Vanna 源码
│       ├── chromadb/              # ChromaDB 向量存储
│       ├── qianwen/               # 通义千问集成
│       └── base/                  # 基础类
│
├── data/                           # 数据目录
│   ├── chroma_db/                 # ChromaDB 向量数据库
│   └── Chinook.sqlite             # SQLite 示例数据库
│
└── static/                         # 静态资源
    ├── assets/                    # 构建后的前端资源
    ├── css/                       # 样式文件
    └── images/                    # 图片资源
```

## 🗄️ 数据库设计

### 核心表结构

#### 1. data_sources (数据源表)
存储所有数据库连接配置信息。

```sql
CREATE TABLE data_sources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,              -- 数据源名称
    type ENUM('mysql', 'sqlite') NOT NULL,   -- 数据源类型
    connection_string TEXT NOT NULL,         -- 连接字符串
    mysql_host VARCHAR(255),                 -- MySQL 主机
    mysql_port INT DEFAULT 3306,             -- MySQL 端口
    mysql_database VARCHAR(255),             -- MySQL 数据库名
    mysql_username VARCHAR(255),             -- MySQL 用户名
    mysql_password VARCHAR(255),             -- MySQL 密码
    sqlite_path TEXT,                        -- SQLite 文件路径
    vector_db_path VARCHAR(255),             -- 向量数据库目录
    is_default BOOLEAN DEFAULT FALSE,        -- 是否为默认数据源
    description TEXT,                        -- 描述
    status VARCHAR(20) DEFAULT 'active',     -- 状态
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### 2. metadata_tables (元数据表)
存储每个数据源的表信息。

```sql
CREATE TABLE metadata_tables (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_source_id INT NOT NULL,             -- 数据源 ID
    table_name VARCHAR(255) NOT NULL,        -- 表名
    table_ddl TEXT,                          -- 建表语句
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (data_source_id) REFERENCES data_sources(id)
);
```

#### 3. metadata_columns (元数据列)
存储每个表的列信息。

```sql
CREATE TABLE metadata_columns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_id INT NOT NULL,                   -- 表 ID
    column_name VARCHAR(255) NOT NULL,       -- 列名
    data_type VARCHAR(100),                  -- 数据类型
    column_description TEXT,                 -- 列描述
    is_primary_key BOOLEAN DEFAULT FALSE,    -- 是否主键
    is_nullable BOOLEAN DEFAULT TRUE,        -- 是否可空
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (table_id) REFERENCES metadata_tables(id)
);
```

## 🔌 API 接口

### 聊天相关

#### POST /api/v0/chat
发送聊天消息，获取 AI 回复。

**请求参数**
```json
{
  "question": "查询销售额最高的前 10 个产品",
  "data_source_id": 1
}
```

**响应示例**
```json
{
  "type": "chat_response",
  "data": {
    "question": "查询销售额最高的前 10 个产品",
    "sql": "SELECT product_name, SUM(sales) as total_sales FROM orders GROUP BY product_name ORDER BY total_sales DESC LIMIT 10",
    "result": [...],
    "chart_type": "bar"
  }
}
```

### 数据源管理

#### GET /api/v0/data_sources
获取所有数据源列表。

**响应示例**
```json
{
  "type": "data_sources",
  "data": [
    {
      "id": 1,
      "name": "MySQL 生产库",
      "type": "mysql",
      "mysql_host": "localhost",
      "mysql_port": 3306,
      "mysql_database": "production",
      "is_default": true,
      "status": "active"
    }
  ]
}
```

#### POST /api/v0/data_sources
添加新数据源。

**请求参数**
```json
{
  "name": "测试数据库",
  "type": "mysql",
  "mysql_host": "localhost",
  "mysql_port": 3306,
  "mysql_database": "test_db",
  "mysql_username": "root",
  "mysql_password": "password",
  "is_default": false,
  "description": "测试环境数据库"
}
```

#### PUT /api/v0/data_sources/:id
更新数据源配置。

#### DELETE /api/v0/data_sources/:id
删除数据源。

#### POST /api/v0/data_sources/:id/test_connection
测试数据库连接。

#### POST /api/v0/data_sources/:id/refresh_metadata
更新数据源的元数据。

### 元数据管理

#### GET /api/v0/data_sources/:dataSourceId/tables
获取指定数据源的所有表。

#### GET /api/v0/data_sources/tables/:tableId/structure
获取表的详细结构（字段信息 + 索引信息）。

## 🎨 前端组件

### 核心组件

#### App.vue
主应用组件，包含：
- 对话界面布局
- 后台管理界面
- 数据源选择器
- 主题切换

#### ChatMessage.vue
聊天消息展示组件，支持：
- 文本消息
- 表格数据
- 图表展示（Plotly）
- SQL 代码展示
- 复制功能

#### ChatInput.vue
聊天输入框组件，支持：
- 多行文本输入
- 发送快捷键（Enter）
- 加载状态
- 禁用状态

#### QuestionList.vue
问题列表组件，用于：
- 展示示例问题
- 展示历史问题
- 问题点击选择

#### DataSourceManager.vue
数据源管理组件，包含：
- 数据源列表表格
- 添加/编辑模态框
- 测试连接功能
- 删除确认对话框

#### DataTable.vue
数据表格组件，支持：
- 动态列渲染
- 数据分页
- 排序
- 导出功能

#### ChartDisplay.vue
图表展示组件，集成：
- Plotly.js
- 多种图表类型
- 交互式图表
- 响应式布局

### 状态管理

#### chat.js (Pinia Store)
管理聊天相关状态：
```javascript
{
  messages: [],              // 聊天消息列表
  isLoading: false,          // 加载状态
  sampleQuestions: [],       // 示例问题
  followupQuestions: [],     // 追问问题
  questionHistory: []        // 问题历史
}
```

## ⚙️ 配置说明

### talktodata.conf 配置文件

```ini
# MySQL 生产环境配置
[mysql]
host = your_mysql_host
port = 3306
user = your_username
password = "your_password"
database = talktodata

# MySQL 开发环境配置
[mysql_dev]
host = your_dev_host
port = 3306
user = your_dev_user
password = "your_dev_password"
database = talktodata

# 大模型服务配置（生产）
[LLM_server]
api_key = your_api_key
model = qwen-plus
options = {"temperature": 0.7}

# 大模型服务配置（开发）
[LLM_server_dev]
api_key = your_dev_api_key
model = qwen-plus
options = {"temperature": 0.7}

# 向量数据库配置
[VectorDB]
base_path = /path/to/chroma_db

[VectorDB_dev]
base_path = D:\path\to\chroma_db
```

### 环境变量

系统会自动加载 `.env` 文件中的环境变量。

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- MySQL 8.0+
- Git

### 1. 克隆项目

```bash
git clone <repository-url>
cd Talk-To-Data
```

### 2. 安装后端依赖

```bash
pip install -r requirements.txt
```

### 3. 安装前端依赖

```bash
cd frontend-vue
npm install
```

### 4. 配置数据库

创建 MySQL 数据库：
```bash
mysql -u root -p < talktodata.sql
```

### 5. 配置应用

编辑 `talktodata.conf` 文件，配置：
- MySQL 连接信息
- 阿里云百炼 API Key
- 向量数据库路径

### 6. 启动后端服务

```bash
python app.py
```

默认访问地址：http://localhost:5000

### 7. 启动前端开发服务器（可选）

```bash
cd frontend-vue
npm run dev
```

开发模式访问地址：http://localhost:5173

### 8. 生产环境部署

前端构建：
```bash
cd frontend-vue
npm run build
```

构建后的文件在 `frontend-vue/dist`，需要复制到 `static` 目录。

## 📖 使用指南

### 1. 首次使用

1. 访问 http://localhost:5000
2. 系统自动选择默认数据源
3. 查看示例问题，了解系统功能
4. 点击示例问题或自行输入问题

### 2. 添加数据源

1. 点击顶部导航栏"后台管理"
2. 选择"数据源管理"
3. 点击"添加数据源"
4. 填写数据源信息
5. 点击"测试连接"验证
6. 勾选"设为默认数据源"（可选）
7. 点击"添加数据源"保存

### 3. 更新元数据

1. 进入"后台管理" → "元数据管理"
2. 点击数据源节点展开库表列表
3. 点击右上角"更新元数据"按钮
4. 等待元数据同步完成

### 4. 查看表结构

1. 在元数据管理中展开数据源
2. 点击具体的表节点
3. 右侧显示表的详细信息：
   - 字段列表（名称、类型、描述）
   - 索引信息
   - DDL 语句

### 5. 切换数据源

1. 在对话界面左侧边栏
2. 顶部"选择数据源"下拉框
3. 选择要使用的数据源
4. 系统自动切换到该数据源

## 📝 开发计划

### 已实现 ✅

- [x] 自然语言查询数据库
- [x] 多数据源支持（MySQL、SQLite）
- [x] 数据源管理（增删改查、测试连接）
- [x] 默认数据源机制
- [x] 元数据管理界面
- [x] 表结构详情展示
- [x] 元数据自动刷新
- [x] DDL 语句存储
- [x] 数据可视化
- [x] 深色模式
- [x] 响应式设计

### 待开发 🚧

- [ ] 知识库管理功能
  - [ ] 训练样本管理
  - [ ] 问题-SQL 对管理
  - [ ] 业务知识库
- [ ] 用户管理功能
  - [ ] 用户列表
  - [ ] 角色权限
  - [ ] 操作日志
- [ ] 高级数据可视化
  - [ ] 更多图表类型
  - [ ] 自定义图表配置
- [ ] 性能优化
  - [ ] 查询缓存优化
  - [ ] 前端懒加载
- [ ] 安全性增强
  - [ ] SQL 注入防护
  - [ ] 访问控制
- [ ] 多语言支持
- [ ] 部署文档完善

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📧 联系方式

如有问题或建议，请通过 Issue 反馈。

---

**最后更新时间**: 2026-04-15
