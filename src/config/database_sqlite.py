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
        # SQLite database path
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'app.db')
        
        # Ensure database directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
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
                        tags TEXT,  -- JSON string of tags array
                        start_time TEXT,  -- ISO format datetime
                        end_time TEXT,    -- ISO format datetime
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
                logger.info("✅ Database tables initialized")
                
        except Exception as e:
            logger.error(f"❌ Failed to initialize database tables: {e}")
    
    def get_connection(self):
        """Get a new database connection"""
        if not self.db_path:
            logger.warning("⚠️ Database not configured!")
            return None
            
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            return conn
        except Exception as e:
            logger.error(f"❌ Failed to connect to SQLite database: {e}")
            return None
    
    def is_connected(self):
        """Check if database is accessible"""
        conn = self.get_connection()
        if conn:
            conn.close()
            return True
        return False

# Global database instance
database = Database()