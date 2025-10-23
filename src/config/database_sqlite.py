import os
import sqlite3
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.db_path = None
        
    def init_app(self, app):
        # SQLite database path - create in the root directory for better Vercel compatibility
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.db_path = os.path.join(project_root, 'database', 'app.db')
        
        # Ensure database directory exists
        db_dir = os.path.dirname(self.db_path)
        os.makedirs(db_dir, exist_ok=True)
        
        # Initialize database tables
        self._init_tables()
        logger.info(f"✅ SQLite database initialized at {self.db_path}")
        
    def _init_tables(self):
        """Initialize database tables if they don't exist"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create notes table
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
                
                # Create users table (if needed)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        created_at TEXT NOT NULL
                    )
                ''')
                
                conn.commit()
                logger.info("✅ Database tables initialized successfully")
                
        except Exception as e:
            logger.error(f"❌ Failed to initialize database tables: {e}")
            raise e
    
    def get_connection(self):
        """Get a new database connection"""
        if not self.db_path:
            logger.error("⚠️ Database path not configured!")
            return None
            
        try:
            # Ensure database file exists
            if not os.path.exists(self.db_path):
                logger.info(f"Creating new database file at {self.db_path}")
                self._init_tables()
            
            conn = sqlite3.connect(self.db_path, timeout=20.0)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            return conn
        except Exception as e:
            logger.error(f"❌ Failed to connect to SQLite database: {e}")
            return None
    
    def is_connected(self):
        """Check if database is accessible"""
        try:
            conn = self.get_connection()
            if conn:
                # Test with a simple query
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()
                conn.close()
                return True
            return False
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False

# Global database instance
database = Database()