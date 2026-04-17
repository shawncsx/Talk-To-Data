import sys
import configparser

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

# 读取配置文件
config_parser = configparser.ConfigParser()
config_parser.read('talktodata.conf', encoding='utf-8')

# 向量数据库配置
vector_db_base_path = config_parser.get('VectorDB_dev', 'base_path') if sys.platform.startswith('win32') else config_parser.get('VectorDB', 'base_path')

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
    mysql_config = {
        "host": config_parser.get('mysql', 'host'),
        "port": config_parser.getint('mysql', 'port'),
        "user": config_parser.get('mysql', 'user'),
        "password": config_parser.get('mysql', 'password'),
        "database": config_parser.get('mysql', 'database')
    } 
    config = {
        "path": chromadb_path, #向量数据库存储路径
        "api_key": config_parser.get('LLM_server', 'api_key'),
        "model": config_parser.get('LLM_server', 'model'),  # 阿里云百炼平台模型
        "options": config_parser.get('LLM_server', 'options'),  # 控制生成随机性
        "initial_prompt": "Please answer me in Chinese.",
        "language": "Chinese"
    }
else:
    chromadb_path=r'D:\shawn\Computer\git\Talk-To-Data\data\chroma_db' 
    sqlite_path=r'D:\shawn\Computer\git\Talk-To-Data\data\Chinook.sqlite'
    # 数据源管理 - 使用ECS MySQL数据库
    mysql_config = {
        "host": config_parser.get('mysql_dev', 'host'),
        "port": config_parser.getint('mysql_dev', 'port'),
        "user": config_parser.get('mysql_dev', 'user'),
        "password": config_parser.get('mysql_dev', 'password'),
        "database": config_parser.get('mysql_dev', 'database')
    }
    config = {
        "path": chromadb_path, #向量数据库存储路径
        "api_key": config_parser.get('LLM_server_dev', 'api_key'),
        "model": config_parser.get('LLM_server_dev', 'model'),  # 阿里云百炼平台模型
        "options": config_parser.get('LLM_server_dev', 'options'),  # 控制生成随机性
        "initial_prompt": "Please answer me in Chinese.",
        "language": "Chinese"
    } 

vn = MyVanna(config=config)
vn.connect_to_sqlite(sqlite_path)

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
            vector_db_path VARCHAR(255),
            description TEXT,
            status VARCHAR(20) DEFAULT 'active',
            is_default BOOLEAN DEFAULT FALSE,
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
                "vector_db_path": chromadb_path,
                "description": "默认的Chinook示例数据库",
                "status": "active"
            }
            
            cursor.execute('''
            INSERT INTO data_sources (name, type, connection_string, sqlite_path, vector_db_path, description, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (
                default_source['name'],
                default_source['type'],
                default_source['connection_string'],
                default_source['sqlite_path'],
                default_source['vector_db_path'],
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
        
        # 检查是否有默认数据源
        has_default = any(source.get('is_default') for source in sources)
        
        # 如果没有默认数据源，将第一个数据源设为默认
        if not has_default and sources:
            first_id = sources[0]['id']
            cursor.execute("UPDATE data_sources SET is_default = TRUE WHERE id = %s", (first_id,))
            conn.commit()
            
            # 重新获取更新后的数据源列表
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
        import os
        sqlite_path = data.get('sqlite_path', '')
        if not os.path.exists(sqlite_path):
            return jsonify({"type": "error", "error": f"SQLite database file does not exist: {sqlite_path}"})
        connection_string = f"sqlite:///{sqlite_path}"
    
    # 自动创建向量数据库目录
    import os
    import shutil
    import hashlib
    
    # 生成唯一的目录名称（基于数据源名称和当前时间）
    import time
    unique_id = hashlib.md5(f"{data['name']}_{time.time()}".encode()).hexdigest()[:8]
    vector_db_dir = os.path.join(vector_db_base_path, f"vectordb_{unique_id}")
    
    # 确保基础目录存在
    if not os.path.exists(vector_db_base_path):
        os.makedirs(vector_db_base_path)
    
    # 创建向量数据库子目录
    if os.path.exists(vector_db_dir):
        shutil.rmtree(vector_db_dir)
    os.makedirs(vector_db_dir)

    # 初始化空的 chromadb 数据库
    # from vanna.chromadb.chromadb_vector import ChromaDB_VectorStore
    # temp_config = {"path": vector_db_dir}
    # temp_chroma = ChromaDB_VectorStore(config=temp_config)
    # temp_chroma.connect()
    
    # 设置 vector_db_path
    data['vector_db_path'] = vector_db_dir
    
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        
        # 如果设置为默认数据源，先将其他所有数据源设置为非默认
        is_default = data.get('is_default', False)
        if is_default:
            cursor.execute("UPDATE data_sources SET is_default = FALSE")
        
        # 插入新数据源
        cursor.execute('''
        INSERT INTO data_sources (name, type, connection_string, mysql_host, mysql_port, mysql_database, mysql_username, mysql_password, sqlite_path, vector_db_path, description, status, is_default)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            data.get('vector_db_path', None),
            data.get('description', ''),
            data.get('status', 'active'),
            1 if is_default else 0
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
        import os
        sqlite_path = data.get('sqlite_path', '')
        if not os.path.exists(sqlite_path):
            return jsonify({"type": "error", "error": f"SQLite database file does not exist: {sqlite_path}"})
        connection_string = f"sqlite:///{sqlite_path}"
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
        if 'vector_db_path' in data:
            update_fields.append("vector_db_path = %s")
            update_values.append(data['vector_db_path'])
        if 'description' in data:
            update_fields.append("description = %s")
            update_values.append(data['description'])
        if 'status' in data:
            update_fields.append("status = %s")
            update_values.append(data['status'])
        if 'is_default' in data:
            # 如果设置为默认数据源，先将其他所有数据源设置为非默认
            if data['is_default']:
                cursor.execute("UPDATE data_sources SET is_default = FALSE WHERE id != %s", (id,))
            update_fields.append("is_default = %s")
            update_values.append(1 if data['is_default'] else 0)
        
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
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        
        # 检查数据源是否存在
        cursor.execute("SELECT * FROM data_sources WHERE id = %s", (id,))
        source = cursor.fetchone()
        
        if not source:
            cursor.close()
            conn.close()
            return jsonify({"type": "error", "error": "Data source not found"})
        
        # 不能删除默认数据源
        if source.get('is_default'):
            cursor.close()
            conn.close()
            return jsonify({"type": "error", "error": "Cannot delete default data source"})
        
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
            import os
            if not os.path.exists(data['sqlite_path']):
                raise Exception(f"SQLite database file does not exist: {data['sqlite_path']}")
            conn = sqlite3.connect(data['sqlite_path'])
            conn.close()
        
        return jsonify({"type": "success", "message": "Connection successful"})
    except Exception as e:
        return jsonify({"type": "error", "error": str(e)})

@app.route('/api/v0/data_sources/<int:data_source_id>/tables', methods=['GET'])
def get_data_source_tables(data_source_id):
    """获取数据源的库表列表"""
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        
        # 从 metadata_tables 表中获取指定数据源的库表
        cursor.execute("SELECT * FROM metadata_tables WHERE data_source_id = %s", (data_source_id,))
        tables = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({"type": "tables", "data": tables})
    except Exception as e:
        return jsonify({"type": "error", "error": str(e)})

@app.route('/api/v0/data_sources/tables/<int:table_id>/structure', methods=['GET'])
def get_table_structure(table_id):
    """获取库表的结构信息"""
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        
        # 获取表的基本信息
        cursor.execute("SELECT * FROM metadata_tables WHERE id = %s", (table_id,))
        table_info = cursor.fetchone()
        
        if not table_info:
            cursor.close()
            conn.close()
            return jsonify({"type": "error", "error": "表不存在"})
        
        # 获取列信息
        cursor.execute("""
            SELECT 
                column_name,
                data_type,
                column_description,
                is_primary_key,
                is_nullable,
                created_at,
                updated_at
            FROM metadata_columns
            WHERE table_id = %s
            ORDER BY id
        """, (table_id,))
        columns = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # 格式化列信息
        formatted_columns = []
        for col in columns:
            formatted_columns.append({
                'name': col['column_name'],
                'type': col['data_type'],
                'description': col['column_description'] or '-',
                'key': 'PRI' if col['is_primary_key'] else '',
                'nullable': bool(col['is_nullable']),
                'default': None,  # 如果需要可以添加默认值字段
                'extra': ''
            })
        
        # 生成索引信息（从主键列生成）
        primary_keys = [col['column_name'] for col in columns if col['is_primary_key']]
        indexes = []
        if primary_keys:
            indexes.append({
                'name': 'PRIMARY',
                'columns': primary_keys,
                'type': 'BTREE'
            })
        
        return jsonify({
            "type": "table_structure",
            "data": {
                "table_info": table_info,
                "columns": formatted_columns,
                "indexes": indexes
            }
        })
    except Exception as e:
        return jsonify({"type": "error", "error": str(e)})

@app.route('/api/v0/data_sources/<int:data_source_id>/refresh_metadata', methods=['POST'])
def refresh_metadata(data_source_id):
    """更新数据源的元数据"""
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        
        # 获取数据源信息
        cursor.execute("SELECT * FROM data_sources WHERE id = %s", (data_source_id,))
        data_source = cursor.fetchone()
        
        if not data_source:
            cursor.close()
            conn.close()
            return jsonify({"type": "error", "error": "数据源不存在"})
        
        # 根据数据源类型连接数据库
        if data_source['type'] == 'mysql':
            # 连接 MySQL 数据库
            db_config = {
                'host': data_source['mysql_host'],
                'port': data_source['mysql_port'],
                'user': data_source['mysql_username'],
                'password': data_source['mysql_password'],
                'database': data_source['mysql_database']
            }
            db_conn = mysql.connector.connect(**db_config)
            db_cursor = db_conn.cursor(dictionary=True)
            
            # 获取所有表
            db_cursor.execute("SHOW TABLES")
            tables = [list(row.values())[0] for row in db_cursor.fetchall()]
            
            # 获取每个表的列信息
            for table_name in tables:
                # 获取表的 DDL
                db_cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
                create_table_row = db_cursor.fetchone()
                table_ddl = list(create_table_row.values())[1] if create_table_row else ''
                
                # 检查表是否已存在于 metadata_tables 中
                cursor.execute("SELECT id FROM metadata_tables WHERE data_source_id = %s AND table_name = %s", 
                             (data_source_id, table_name))
                existing_table = cursor.fetchone()
                
                if existing_table:
                    table_id = existing_table['id']
                    # 更新表信息（包括 DDL）
                    cursor.execute("""
                        UPDATE metadata_tables 
                        SET table_name = %s, table_ddl = %s, updated_at = NOW()
                        WHERE id = %s
                    """, (table_name, table_ddl, table_id))
                    
                    # 删除旧的列信息
                    cursor.execute("DELETE FROM metadata_columns WHERE table_id = %s", (table_id,))
                else:
                    # 插入新表信息（包括 DDL）
                    cursor.execute("""
                        INSERT INTO metadata_tables (data_source_id, table_name, table_ddl, created_at, updated_at)
                        VALUES (%s, %s, %s, NOW(), NOW())
                    """, (data_source_id, table_name, table_ddl))
                    table_id = cursor.lastrowid
                
                # 获取列信息
                db_cursor.execute(f"SHOW FULL COLUMNS FROM `{table_name}`")
                columns = db_cursor.fetchall()
                
                # 插入列信息
                for col in columns:
                    is_primary = 'PRI' in col.get('Key', '')
                    is_nullable = col.get('Null', 'YES') == 'YES'
                    
                    cursor.execute("""
                        INSERT INTO metadata_columns 
                        (table_id, column_name, data_type, column_description, is_primary_key, is_nullable, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
                    """, (
                        table_id,
                        col['Field'],
                        col['Type'],
                        col.get('Comment', ''),
                        1 if is_primary else 0,
                        1 if is_nullable else 0
                    ))
            
            db_cursor.close()
            db_conn.close()
            
            # 提交事务
            conn.commit()
        elif data_source['type'] == 'sqlite':
            import sqlite3
            
            # 连接 SQLite 数据库
            sqlite_path = data_source['sqlite_path']
            db_conn = sqlite3.connect(sqlite_path)
            db_cursor = db_conn.cursor()
            
            # 获取所有表
            db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in db_cursor.fetchall()]
            
            # 获取每个表的列信息
            for table_name in tables:
                # 获取表的 DDL
                db_cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
                ddl_row = db_cursor.fetchone()
                table_ddl = ddl_row[0] if ddl_row else ''
                
                # 检查表是否已存在于 metadata_tables 中
                cursor.execute("SELECT id FROM metadata_tables WHERE data_source_id = %s AND table_name = %s", 
                             (data_source_id, table_name))
                existing_table = cursor.fetchone()
                
                if existing_table:
                    table_id = existing_table['id']
                    # 更新表信息（包括 DDL）
                    cursor.execute("""
                        UPDATE metadata_tables 
                        SET table_name = %s, table_ddl = %s, updated_at = NOW()
                        WHERE id = %s
                    """, (table_name, table_ddl, table_id))
                    
                    # 删除旧的列信息
                    cursor.execute("DELETE FROM metadata_columns WHERE table_id = %s", (table_id,))
                else:
                    # 插入新表信息（包括 DDL）
                    cursor.execute("""
                        INSERT INTO metadata_tables (data_source_id, table_name, table_ddl, created_at, updated_at)
                        VALUES (%s, %s, %s, NOW(), NOW())
                    """, (data_source_id, table_name, table_ddl))
                    table_id = cursor.lastrowid
                
                # 获取列信息
                db_cursor.execute(f"PRAGMA table_info({table_name})")
                columns = db_cursor.fetchall()
                
                # 插入列信息
                for col in columns:
                    # col: (cid, name, type, notnull, dflt_value, pk)
                    cid, col_name, col_type, notnull, dflt_value, pk = col
                    is_primary = pk == 1
                    is_nullable = notnull == 0
                    
                    cursor.execute("""
                        INSERT INTO metadata_columns 
                        (table_id, column_name, data_type, column_description, is_primary_key, is_nullable, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
                    """, (
                        table_id,
                        col_name,
                        col_type,
                        '',  # SQLite 没有注释字段
                        1 if is_primary else 0,
                        1 if is_nullable else 0
                    ))
            
            db_cursor.close()
            db_conn.close()
            
            # 提交事务
            conn.commit()
        else:
            cursor.close()
            conn.close()
            return jsonify({"type": "error", "error": "不支持的数据源类型"})
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "type": "success",
            "message": f"已更新 {len(tables)} 个表的元数据"
        })
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