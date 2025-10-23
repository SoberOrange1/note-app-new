import os
from flask_pymongo import PyMongo
from pymongo import MongoClient
from datetime import datetime
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

class Database:
    def __init__(self):
        self.mongo = None
        self.db = None
        self.connected = False
        self.mongodb_uri = None
        
    def init_app(self, app):
        # MongoDB Atlas connection string from environment variables
        self.mongodb_uri = os.environ.get('MONGODB_URI')
        
        if not self.mongodb_uri:
            logger.error("❌ MONGODB_URI environment variable not set!")
            return
            
        if '<username>' in self.mongodb_uri or '<password>' in self.mongodb_uri:
            logger.error("❌ Please replace placeholder values in your MONGODB_URI!")
            return
        
        app.config['MONGO_URI'] = self.mongodb_uri
        
        # For serverless, we'll create connections on-demand rather than persistent connections
        logger.info("✅ Database configuration initialized for serverless environment")
        
    def get_db(self):
        """Get database connection - creates new connection each time for serverless"""
        if not self.mongodb_uri:
            logger.warning("⚠️ MongoDB URI not configured!")
            return None
            
        try:
            # Create a new connection each time (better for serverless)
            client = MongoClient(
                self.mongodb_uri,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=5000,
                maxPoolSize=1,
                retryWrites=True
            )
            
            # Test the connection
            client.admin.command('ping')
            db = client.get_database()  # Gets the database from the URI
            
            logger.info("✅ MongoDB connection successful")
            return db
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            return None
    
    def is_connected(self):
        """Check if we can connect to MongoDB"""
        db = self.get_db()
        return db is not None

# Global database instance
database = Database()