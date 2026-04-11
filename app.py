import sys

from dotenv import load_dotenv
load_dotenv()

from functools import wraps
from flask import Flask, jsonify, Response, request, redirect, url_for
import flask
import os
from cache import MemoryCache
import mysql.connector
import sqlite3
import json

app = Flask(__name__, static_url_path='')
# app = Flask(__name__, static_url_path='', static_folder='static-vue')

# SETUP
cache = MemoryCache()

from vanna.chromadb.chromadb_vector import ChromaDB_VectorStore
from vanna.qianwen.QianwenAI_chat import QianWenAI_Chat

class MyVanna(ChromaDB_VectorStore, QianWenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        QianWenAI_Chat.__init__(self, config=config)

if sys.platform.startswith("linux"):
    chromadb_path=r"/root/app_files/TalkToData/data/chroma_db"
    sqlite_path=r"/root/app_files/TalkToData/data/Chinook.sqlite"
else:
    chromadb_path=r'D:\shawn\Computer\git\Talk-To-Data\data\chroma_db' 
    sqlite_path=r'D:\shawn\Computer\git\Talk-To-Data\data\Chinook.sqlite'    

config = {
    "path": chromadb_path, #向量数据库存储路径
    "api_key": "sk-10ac90a6267a46ad83df797d65520494",
    "model": "qwen-plus",  # 阿里云百炼平台模型
    "options": {"temperature": 0.3},  # 控制生成随机性
    "initial_prompt": "Please answer me in Chinese."
}

vn = MyVanna(config=config)
vn.connect_to_sqlite(sqlite_path)

# 数据源管理 - 使用ECS MySQL数据库
mysql_config = {
    "host": "47.120.40.157",
    "port": 3306,
    "user": "root",
    "password": "Shawn#6ge1",
    "database": "talktodata"
}

# 初始化MySQL连接
def init_mysql_connection():
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        
        # 创建data_sources表（如果不存在）
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS data_sources (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            type ENUM('mysql', 'sqlite') NOT NULL,
            connection_string TEXT NOT NULL,
            mysql_host VARCHAR(255),
            mysql_port INT DEFAULT 3306,
            mysql_database VARCHAR(255),
            mysql_username VARCHAR(255),
            mysql_password VARCHAR(255),
            sqlite_path TEXT,
            description TEXT,
            status VARCHAR(20) DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        ''')
        
        # 检查是否有默认数据源
        cursor.execute("SELECT COUNT(*) FROM data_sources WHERE id = 1")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # 插入默认SQLite数据源
            default_source = {
                "name": "默认SQLite数据库",
                "type": "sqlite",
                "connection_string": f"sqlite:///{sqlite_path}",
                "sqlite_path": sqlite_path,
                "description": "默认的Chinook示例数据库",
                "status": "active"
            }
            
            cursor.execute('''
            INSERT INTO data_sources (name, type, connection_string, sqlite_path, description, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            ''', (
                default_source['name'],
                default_source['type'],
                default_source['connection_string'],
                default_source['sqlite_path'],
                default_source['description'],
                default_source['status']
            ))
            conn.commit()
        
        cursor.close()
        conn.close()
        print("MySQL database initialized successfully")
    except Exception as e:
        print(f"Error initializing MySQL database: {e}")

# 初始化MySQL数据库
init_mysql_connection()

# 数据源管理API
@app.route('/api/v0/data_sources', methods=['GET'])
def get_data_sources():
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM data_sources")
        sources = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({"type": "data_sources", "data": sources})
    except Exception as e:
        return jsonify({"type": "error", "error": str(e)})

@app.route('/api/v0/data_sources', methods=['POST'])
def add_data_source():
    data = request.json
    
    # 验证必填字段
    required_fields = ['name', 'type']
    for field in required_fields:
        if field not in data:
            return jsonify({"type": "error", "error": f"Missing required field: {field}"})
    
    # 构建连接字符串
    if data['type'] == 'mysql':
        connection_string = f"mysql://{data.get('mysql_username', '')}:{data.get('mysql_password', '')}@{data.get('mysql_host', '')}:{data.get('mysql_port', 3306)}/{data.get('mysql_database', '')}"
    elif data['type'] == 'sqlite':
        connection_string = f"sqlite:///{data.get('sqlite_path', '')}"
    
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        
        # 插入新数据源
        cursor.execute('''
        INSERT INTO data_sources (name, type, connection_string, mysql_host, mysql_port, mysql_database, mysql_username, mysql_password, sqlite_path, description, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            data['name'],
            data['type'],
            connection_string,
            data.get('mysql_host', None),
            data.get('mysql_port', 3306),
            data.get('mysql_database', None),
            data.get('mysql_username', None),
            data.get('mysql_password', None),
            data.get('sqlite_path', None),
            data.get('description', ''),
            data.get('status', 'active')
        ))
        
        conn.commit()
        new_id = cursor.lastrowid
        
        # 获取新插入的数据源
        cursor.execute("SELECT * FROM data_sources WHERE id = %s", (new_id,))
        new_source = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return jsonify({"type": "success", "data": new_source})
    except Exception as e:
        return jsonify({"type": "error", "error": str(e)})

@app.route('/api/v0/data_sources/<int:id>', methods=['PUT'])
def update_data_source(id):
    data = request.json
    
    # 构建连接字符串
    if data.get('type') == 'mysql':
        connection_string = f"mysql://{data.get('mysql_username', '')}:{data.get('mysql_password', '')}@{data.get('mysql_host', '')}:{data.get('mysql_port', 3306)}/{data.get('mysql_database', '')}"
    elif data.get('type') == 'sqlite':
        connection_string = f"sqlite:///{data.get('sqlite_path', '')}"
    else:
        # 如果类型没有变化，保持原有连接字符串
        connection_string = None
    
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        
        # 检查数据源是否存在
        cursor.execute("SELECT * FROM data_sources WHERE id = %s", (id,))
        existing_source = cursor.fetchone()
        
        if not existing_source:
            cursor.close()
            conn.close()
            return jsonify({"type": "error", "error": "Data source not found"})
        
        # 更新数据源
        update_fields = []
        update_values = []
        
        if 'name' in data:
            update_fields.append("name = %s")
            update_values.append(data['name'])
        if 'type' in data:
            update_fields.append("type = %s")
            update_values.append(data['type'])
        if connection_string:
            update_fields.append("connection_string = %s")
            update_values.append(connection_string)
        if 'mysql_host' in data:
            update_fields.append("mysql_host = %s")
            update_values.append(data['mysql_host'])
        if 'mysql_port' in data:
            update_fields.append("mysql_port = %s")
            update_values.append(data['mysql_port'])
        if 'mysql_database' in data:
            update_fields.append("mysql_database = %s")
            update_values.append(data['mysql_database'])
        if 'mysql_username' in data:
            update_fields.append("mysql_username = %s")
            update_values.append(data['mysql_username'])
        if 'mysql_password' in data:
            update_fields.append("mysql_password = %s")
            update_values.append(data['mysql_password'])
        if 'sqlite_path' in data:
            update_fields.append("sqlite_path = %s")
            update_values.append(data['sqlite_path'])
        if 'description' in data:
            update_fields.append("description = %s")
            update_values.append(data['description'])
        if 'status' in data:
            update_fields.append("status = %s")
            update_values.append(data['status'])
        
        if update_fields:
            update_query = f"UPDATE data_sources SET {', '.join(update_fields)} WHERE id = %s"
            update_values.append(id)
            
            cursor.execute(update_query, update_values)
            conn.commit()
        
        # 获取更新后的数据源
        cursor.execute("SELECT * FROM data_sources WHERE id = %s", (id,))
        updated_source = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return jsonify({"type": "success", "data": updated_source})
    except Exception as e:
        return jsonify({"type": "error", "error": str(e)})

@app.route('/api/v0/data_sources/<int:id>', methods=['DELETE'])
def delete_data_source(id):
    # 不能删除默认数据源
    if id == 1:
        return jsonify({"type": "error", "error": "Cannot delete default data source"})
    
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        
        # 检查数据源是否存在
        cursor.execute("SELECT * FROM data_sources WHERE id = %s", (id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"type": "error", "error": "Data source not found"})
        
        # 删除数据源
        cursor.execute("DELETE FROM data_sources WHERE id = %s", (id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({"type": "success", "message": "Data source deleted successfully"})
    except Exception as e:
        return jsonify({"type": "error", "error": str(e)})

@app.route('/api/v0/data_sources/test', methods=['POST'])
def test_data_source():
    data = request.json
    
    try:
        if data['type'] == 'mysql':
            # 测试MySQL连接
            conn = mysql.connector.connect(
                host=data['mysql_host'],
                port=data['mysql_port'],
                user=data['mysql_username'],
                password=data['mysql_password'],
                database=data['mysql_database']
            )
            conn.close()
        elif data['type'] == 'sqlite':
            # 测试SQLite连接
            conn = sqlite3.connect(data['sqlite_path'])
            conn.close()
        
        return jsonify({"type": "success", "message": "Connection successful"})
    except Exception as e:
        return jsonify({"type": "error", "error": str(e)})

######################################################################################

# NO NEED TO CHANGE ANYTHING BELOW THIS LINE
def requires_cache(fields):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            id = request.args.get('id')

            if id is None:
                return jsonify({"type": "error", "error": "No id provided"})
            
            for field in fields:
                if cache.get(id=id, field=field) is None:
                    return jsonify({"type": "error", "error": f"No {field} found"})
            
            field_values = {field: cache.get(id=id, field=field) for field in fields}
            
            # Add the id to the field_values
            field_values['id'] = id

            return f(*args, **field_values, **kwargs)
        return decorated
    return decorator

@app.route('/api/v0/generate_questions', methods=['GET'])
def generate_questions():
    return jsonify({
        "type": "question_list", 
        "questions": vn.generate_questions(),
        "header": "Here are some questions you can ask:"
        })

@app.route('/api/v0/generate_sql', methods=['GET'])
def generate_sql():
    question = flask.request.args.get('question')

    if question is None:
        return jsonify({"type": "error", "error": "No question provided"})

    id = cache.generate_id(question=question)
    sql = vn.generate_sql(question=question)

    cache.set(id=id, field='question', value=question)
    cache.set(id=id, field='sql', value=sql)

    return jsonify(
        {
            "type": "sql", 
            "id": id,
            "text": sql,
        })

@app.route('/api/v0/run_sql', methods=['GET'])
@requires_cache(['sql'])
def run_sql(id: str, sql: str):
    try:
        df = vn.run_sql(sql=sql)

        cache.set(id=id, field='df', value=df)

        return jsonify(
            {
                "type": "df", 
                "id": id,
                "df": df.head(10).to_json(orient='records'),
            })

    except Exception as e:
        return jsonify({"type": "error", "error": str(e)})

@app.route('/api/v0/download_csv', methods=['GET'])
@requires_cache(['df'])
def download_csv(id: str, df):
    csv = df.to_csv()

    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 f"attachment; filename={id}.csv"})

@app.route('/api/v0/generate_plotly_figure', methods=['GET'])
@requires_cache(['df', 'question', 'sql'])
def generate_plotly_figure(id: str, df, question, sql):
    try:
        code = vn.generate_plotly_code(question=question, sql=sql, df_metadata=f"Running df.dtypes gives:\n {df.dtypes}")
        fig = vn.get_plotly_figure(plotly_code=code, df=df, dark_mode=False)
        fig_json = fig.to_json()

        cache.set(id=id, field='fig_json', value=fig_json)

        return jsonify(
            {
                "type": "plotly_figure", 
                "id": id,
                "fig": fig_json,
            })
    except Exception as e:
        # Print the stack trace
        import traceback
        traceback.print_exc()

        return jsonify({"type": "error", "error": str(e)})

@app.route('/api/v0/get_training_data', methods=['GET'])
def get_training_data():
    df = vn.get_training_data()

    return jsonify(
    {
        "type": "df", 
        "id": "training_data",
        "df": df.head(25).to_json(orient='records'),
    })

@app.route('/api/v0/remove_training_data', methods=['POST'])
def remove_training_data():
    # Get id from the JSON body
    id = flask.request.json.get('id')

    if id is None:
        return jsonify({"type": "error", "error": "No id provided"})

    if vn.remove_training_data(id=id):
        return jsonify({"success": True})
    else:
        return jsonify({"type": "error", "error": "Couldn't remove training data"})

@app.route('/api/v0/train', methods=['POST'])
def add_training_data():
    question = flask.request.json.get('question')
    sql = flask.request.json.get('sql')
    ddl = flask.request.json.get('ddl')
    documentation = flask.request.json.get('documentation')

    try:
        id = vn.train(question=question, sql=sql, ddl=ddl, documentation=documentation)

        return jsonify({"id": id})
    except Exception as e:
        print("TRAINING ERROR", e)
        return jsonify({"type": "error", "error": str(e)})

@app.route('/api/v0/generate_followup_questions', methods=['GET'])
@requires_cache(['df', 'question', 'sql'])
def generate_followup_questions(id: str, df, question, sql):
    followup_questions = vn.generate_followup_questions(question=question, sql=sql, df=df)

    cache.set(id=id, field='followup_questions', value=followup_questions)

    return jsonify(
        {
            "type": "question_list", 
            "id": id,
            "questions": followup_questions,
            "header": "Here are some followup questions you can ask:"
        })

@app.route('/api/v0/load_question', methods=['GET'])
@requires_cache(['question', 'sql', 'df', 'fig_json', 'followup_questions'])
def load_question(id: str, question, sql, df, fig_json, followup_questions):
    try:
        return jsonify(
            {
                "type": "question_cache", 
                "id": id,
                "question": question,
                "sql": sql,
                "df": df.head(10).to_json(orient='records'),
                "fig": fig_json,
                "followup_questions": followup_questions,
            })

    except Exception as e:
        return jsonify({"type": "error", "error": str(e)})

@app.route('/api/v0/get_question_history', methods=['GET'])
def get_question_history():
    return jsonify({"type": "question_history", "questions": cache.get_all(field_list=['question']) })

@app.route('/')
def root():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=False)