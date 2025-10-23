import os
import sqlite3
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.is_production = os.environ.get('VERCEL') == '1' or os.environ.get('FLASK_ENV') == 'production'
        
    def init_app(self, app):
        if self.is_production:
            logger.info("🔥 Vercel deployment - using in-memory database")
        else:
            logger.info("💽 Local development - using file database")
        
    def get_connection(self):
        """获取数据库连接"""
        try:
            if self.is_production:
                # Vercel: 使用内存数据库，每次都重新创建
                conn = sqlite3.connect(':memory:')
                conn.row_factory = sqlite3.Row
                
                # 创建表结构
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE notes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        tags TEXT DEFAULT '[]',
                        start_time TEXT,
                        end_time TEXT,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                ''')
                conn.commit()
                return conn
            else:
                # 本地开发：使用文件数据库
                project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                db_path = os.path.join(project_root, 'database', 'app.db')
                
                # 确保目录存在
                os.makedirs(os.path.dirname(db_path), exist_ok=True)
                
                conn = sqlite3.connect(db_path)
                conn.row_factory = sqlite3.Row
                
                # 创建表结构（如果不存在）
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS notes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        tags TEXT DEFAULT '[]',
                        start_time TEXT,
                        end_time TEXT,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                ''')
                conn.commit()
                return conn
                
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            return None
    
    def is_connected(self):
        """检查数据库连接"""
        try:
            conn = self.get_connection()
            if conn:
                conn.close()
                return True
            return False
        except:
            return False

# Global database instance
database = Database()