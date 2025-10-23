# MONGODB CONFIGURATION - COMMENTED OUT
# This file is no longer used - we switched to SQLite
# All MongoDB related code has been disabled

# import os
# from flask_pymongo import PyMongo
# from pymongo import MongoClient
# from datetime import datetime
# import logging
# from dotenv import load_dotenv
# import ssl

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Load environment variables from .env file
# load_dotenv()

# class Database:
#     def __init__(self):
#         self.mongo = None
#         self.db = None
#         self.connected = False
#         self.client = None
        
#     def init_app(self, app):
#         # MongoDB Atlas connection string from environment variables
#         mongodb_uri = os.environ.get('MONGODB_URI')
        
#         if not mongodb_uri:
#             logger.error("❌ MONGODB_URI environment variable not set!")
#             # For deployment debugging, try to continue with a default
#             mongodb_uri = "mongodb+srv://theorangejeff20_db_user:EcKBVf2b00yIEiFQ@noteapp.gppinh1.mongodb.net/notetaker?retryWrites=true&w=majority&appName=NoteApp"
#             logger.warning("⚠️ Using fallback MongoDB URI")
            
#         if '<username>' in mongodb_uri or '<password>' in mongodb_uri or '<cluster>' in mongodb_uri:
#             logger.error("❌ Please replace placeholder values in your MONGODB_URI!")
#             return
        
#         # Configure for Vercel's serverless environment
#         app.config['MONGO_URI'] = mongodb_uri
        
#         try:
#             # Try direct PyMongo connection first for better error handling
#             self.client = MongoClient(
#                 mongodb_uri,
#                 serverSelectionTimeoutMS=10000,  # 10 second timeout
#                 connectTimeoutMS=10000,
#                 maxPoolSize=1,  # Important for serverless
#                 retryWrites=True,
#                 ssl=True,
#                 ssl_cert_reqs=ssl.CERT_NONE
#             )
            
#             # Test the connection
#             self.client.admin.command('ping')
            
#             # Now set up Flask-PyMongo
#             self.mongo = PyMongo(app)
#             self.db = self.mongo.db
            
#             self.connected = True
#             logger.info("✅ Successfully connected to MongoDB Atlas!")
            
#         except Exception as e:
#             logger.error(f"❌ Failed to connect to MongoDB Atlas: {e}")
#             self.connected = False
#             self.db = None
#             self.client = None
            
#             # Try fallback connection method
#             try:
#                 logger.info("Attempting fallback connection...")
#                 self.mongo = PyMongo(app)
#                 self.db = self.mongo.db
#                 self.db.command('ping')
#                 self.connected = True
#                 logger.info("✅ Fallback connection successful!")
#             except Exception as fallback_error:
#                 logger.error(f"❌ Fallback connection also failed: {fallback_error}")
    
#     def reconnect_if_needed(self):
#         """Try to reconnect if connection is lost"""
#         if not self.connected:
#             try:
#                 if self.client:
#                     self.client.admin.command('ping')
#                     self.connected = True
#                 elif self.db:
#                     self.db.command('ping')
#                     self.connected = True
#             except Exception as e:
#                 logger.warning(f"Reconnection attempt failed: {e}")
#                 self.connected = False
            
#     def get_db(self):
#         # Try to reconnect if not connected
#         if not self.connected:
#             self.reconnect_if_needed()
            
#         if not self.connected or self.db is None:
#             logger.warning("⚠️ Database not available!")
#             return None
#         return self.db
    
#     def is_connected(self):
#         # Check connection status
#         self.reconnect_if_needed()
#         return self.connected and self.db is not None

# # Global database instance
# database = Database()

print("⚠️ MongoDB database.py is disabled - using SQLite instead")