# MONGODB USER MODEL - COMMENTED OUT
# This file is no longer used - we switched to SQLite
# All MongoDB related code has been disabled

# from datetime import datetime
# from bson import ObjectId
# from src.config.database import database

# class User:
#     def __init__(self, username=None, email=None, _id=None, created_at=None, updated_at=None):
#         self._id = _id
#         self.username = username
#         self.email = email
#         self.created_at = created_at or datetime.utcnow()
#         self.updated_at = updated_at or datetime.utcnow()
    
#     @staticmethod
#     def get_collection():
#         """Get the users collection from MongoDB"""
#         return database.get_db().users
    
#     def save(self):
#         """Save the user to MongoDB"""
#         collection = self.get_collection()
#         user_data = {
#             'username': self.username,
#             'email': self.email,
#             'created_at': self.created_at,
#             'updated_at': datetime.utcnow()
#         }
        
#         if self._id:
#             # Update existing user
#             collection.update_one(
#                 {'_id': ObjectId(self._id)},
#                 {'$set': user_data}
#             )
#         else:
#             # Create new user
#             user_data['created_at'] = self.created_at
#             result = collection.insert_one(user_data)
#             self._id = str(result.inserted_id)
        
#         self.updated_at = user_data['updated_at']
#         return self
    
#     @classmethod
#     def find_all(cls):
#         """Get all users"""
#         collection = cls.get_collection()
#         users = collection.find().sort('created_at', -1)
#         return [cls.from_dict(user) for user in users]
    
#     @classmethod
#     def find_by_id(cls, user_id):
#         """Find a user by ID"""
#         try:
#             collection = cls.get_collection()
#             user = collection.find_one({'_id': ObjectId(user_id)})
#             return cls.from_dict(user) if user else None
#         except:
#             return None
    
#     @classmethod
#     def find_by_username(cls, username):
#         """Find a user by username"""
#         collection = cls.get_collection()
#         user = collection.find_one({'username': username})
#         return cls.from_dict(user) if user else None
    
#     @classmethod
#     def find_by_email(cls, email):
#         """Find a user by email"""
#         collection = cls.get_collection()
#         user = collection.find_one({'email': email})
#         return cls.from_dict(user) if user else None
    
#     def delete(self):
#         """Delete the user from MongoDB"""
#         if self._id:
#             collection = self.get_collection()
#             collection.delete_one({'_id': ObjectId(self._id)})
#             return True
#         return False
    
#     @classmethod
#     def from_dict(cls, data):
#         """Create User instance from dictionary"""
#         if not data:
#             return None
#         return cls(
#             _id=str(data['_id']),
#             username=data.get('username', ''),
#             email=data.get('email', ''),
#             created_at=data.get('created_at'),
#             updated_at=data.get('updated_at')
#         )
    
#     def to_dict(self):
#         """Convert User instance to dictionary"""
#         return {
#             'id': self._id,
#             'username': self.username,
#             'email': self.email,
#             'created_at': self.created_at.isoformat() if self.created_at else None,
#             'updated_at': self.updated_at.isoformat() if self.updated_at else None
#         }
    
#     def __repr__(self):
#         return f'<User {self.username}>'

print("⚠️ MongoDB user.py is disabled - using SQLite user_sqlite.py instead")
