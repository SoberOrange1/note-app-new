import sqlite3
import json
from datetime import datetime
from src.config.database_sqlite import database
import logging

logger = logging.getLogger(__name__)

class User:
    def __init__(self, username=None, email=None, password_hash=None, _id=None, created_at=None, updated_at=None):
        self._id = _id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def save(self):
        """Save the user to SQLite database"""
        conn = None
        try:
            conn = database.get_connection()
            if not conn:
                raise Exception("Database connection not available")
                
            cursor = conn.cursor()
            
            # Convert datetime to ISO string
            updated_at_str = datetime.utcnow().isoformat()
            
            if self._id:
                # Update existing user
                cursor.execute('''
                    UPDATE users SET 
                    username = ?, email = ?, password_hash = ?, updated_at = ?
                    WHERE id = ?
                ''', (self.username, self.email, self.password_hash, updated_at_str, self._id))
                
                if cursor.rowcount == 0:
                    raise Exception(f"User with id {self._id} not found")
            else:
                # Create new user
                created_at_str = self.created_at.isoformat()
                cursor.execute('''
                    INSERT INTO users (username, email, password_hash, created_at)
                    VALUES (?, ?, ?, ?)
                ''', (self.username, self.email, self.password_hash, created_at_str))
                
                self._id = cursor.lastrowid
            
            conn.commit()
            self.updated_at = datetime.fromisoformat(updated_at_str)
            logger.info(f"✅ User saved successfully with ID: {self._id}")
            return self
            
        except Exception as e:
            error_msg = f"Error saving user: {e}"
            logger.error(error_msg)
            if conn:
                conn.rollback()
            raise Exception(error_msg)
        finally:
            if conn:
                conn.close()
    
    @classmethod
    def find_all(cls):
        """Get all users, ordered by most recently created"""
        try:
            conn = database.get_connection()
            if not conn:
                return []
                
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
            rows = cursor.fetchall()
            conn.close()
            
            return [cls.from_dict(dict(row)) for row in rows]
            
        except Exception as e:
            logger.error(f"Error finding all users: {e}")
            return []
    
    @classmethod
    def find_by_id(cls, user_id):
        """Find a user by ID"""
        try:
            conn = database.get_connection()
            if not conn:
                return None
                
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            conn.close()
            
            return cls.from_dict(dict(row)) if row else None
            
        except Exception as e:
            logger.error(f"Error finding user by ID: {e}")
            return None
    
    @classmethod
    def find_by_username(cls, username):
        """Find a user by username"""
        try:
            conn = database.get_connection()
            if not conn:
                return None
                
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            row = cursor.fetchone()
            conn.close()
            
            return cls.from_dict(dict(row)) if row else None
            
        except Exception as e:
            logger.error(f"Error finding user by username: {e}")
            return None
    
    @classmethod
    def find_by_email(cls, email):
        """Find a user by email"""
        try:
            conn = database.get_connection()
            if not conn:
                return None
                
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            row = cursor.fetchone()
            conn.close()
            
            return cls.from_dict(dict(row)) if row else None
            
        except Exception as e:
            logger.error(f"Error finding user by email: {e}")
            return None
    
    def delete(self):
        """Delete the user from SQLite database"""
        try:
            if not self._id:
                return False
                
            conn = database.get_connection()
            if not conn:
                return False
                
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE id = ?', (self._id,))
            success = cursor.rowcount > 0
            conn.commit()
            conn.close()
            
            return success
            
        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            return False
    
    @classmethod
    def from_dict(cls, data):
        """Create User instance from dictionary"""
        if not data:
            return None
        
        # Parse datetime strings
        created_at = None
        updated_at = None
        
        if data.get('created_at'):
            try:
                created_at = datetime.fromisoformat(data['created_at'])
            except:
                pass
                
        if data.get('updated_at'):
            try:
                updated_at = datetime.fromisoformat(data['updated_at'])
            except:
                pass
        
        return cls(
            _id=data.get('id'),
            username=data.get('username', ''),
            email=data.get('email', ''),
            password_hash=data.get('password_hash', ''),
            created_at=created_at,
            updated_at=updated_at
        )
    
    def to_dict(self):
        """Convert User instance to dictionary"""
        return {
            'id': self._id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'