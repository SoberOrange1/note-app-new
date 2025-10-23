import os
from flask_pymongo import PyMongo
from pymongo import MongoClient
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Database:
    def __init__(self):
        self.mongo = None
        self.db = None
        
    def init_app(self, app):
        # MongoDB Atlas connection string from environment variables
        mongodb_uri = os.environ.get('MONGODB_URI')
        
        if not mongodb_uri:
            print("❌ MONGODB_URI environment variable not set!")
            logging.error("MONGODB_URI environment variable not set")
            return
            
        if '<username>' in mongodb_uri or '<password>' in mongodb_uri or '<cluster>' in mongodb_uri:
            print("❌ Please replace placeholder values in your MONGODB_URI!")
            logging.error("MongoDB URI contains placeholder values")
            return
        
        app.config['MONGO_URI'] = mongodb_uri
        
        try:
            self.mongo = PyMongo(app)
            self.db = self.mongo.db
            
            # Test connection
            self.db.command('ping')
            print("✅ Successfully connected to MongoDB Atlas!")
            
        except Exception as e:
            print(f"❌ Failed to connect to MongoDB Atlas: {e}")
            logging.error(f"MongoDB connection error: {e}")
            
    def get_db(self):
        return self.db

# Global database instance
database = Database()