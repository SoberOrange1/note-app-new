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
        
    def init_app(self, app):
        # MongoDB Atlas connection string from environment variables
        mongodb_uri = os.environ.get('MONGODB_URI')
        
        if not mongodb_uri:
            logger.error("❌ MONGODB_URI environment variable not set!")
            # For deployment debugging, try to continue with a default
            mongodb_uri = "mongodb+srv://theorangejeff20_db_user:EcKBVf2b00yIEiFQ@noteapp.gppinh1.mongodb.net/notetaker?retryWrites=true&w=majority&appName=NoteApp"
            logger.warning("⚠️ Using fallback MongoDB URI")
            
        if '<username>' in mongodb_uri or '<password>' in mongodb_uri or '<cluster>' in mongodb_uri:
            logger.error("❌ Please replace placeholder values in your MONGODB_URI!")
            return
        
        app.config['MONGO_URI'] = mongodb_uri
        
        try:
            self.mongo = PyMongo(app)
            self.db = self.mongo.db
            
            # Test connection with timeout
            self.db.command('ping')
            self.connected = True
            logger.info("✅ Successfully connected to MongoDB Atlas!")
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to MongoDB Atlas: {e}")
            self.connected = False
            # Set db to None to indicate connection failure
            self.db = None
            
    def get_db(self):
        if not self.connected or self.db is None:
            logger.warning("⚠️ Database not available!")
            return None
        return self.db
    
    def is_connected(self):
        return self.connected and self.db is not None

# Global database instance
database = Database()