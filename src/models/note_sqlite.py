import sqlite3
import json
from datetime import datetime
from src.config.database_sqlite import database
import logging

logger = logging.getLogger(__name__)

class Note:
    def __init__(self, title=None, content=None, tags=None, start_time=None, end_time=None, _id=None, created_at=None, updated_at=None):
        self._id = _id
        self.title = title
        self.content = content
        self.tags = tags or []
        self.start_time = start_time
        self.end_time = end_time
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def save(self):
        """Save the note to SQLite database"""
        conn = None
        try:
            conn = database.get_connection()
            if not conn:
                raise Exception("Database connection not available")
                
            cursor = conn.cursor()
            
            # Convert tags list to JSON string
            tags_json = json.dumps(self.tags) if self.tags else '[]'
            
            # Convert datetime to ISO string
            start_time_str = self.start_time.isoformat() if self.start_time else None
            end_time_str = self.end_time.isoformat() if self.end_time else None
            updated_at_str = datetime.utcnow().isoformat()
            
            if self._id:
                # Update existing note
                cursor.execute('''
                    UPDATE notes SET 
                    title = ?, content = ?, tags = ?, 
                    start_time = ?, end_time = ?, updated_at = ?
                    WHERE id = ?
                ''', (self.title, self.content, tags_json, 
                     start_time_str, end_time_str, updated_at_str, self._id))
                
                if cursor.rowcount == 0:
                    raise Exception(f"Note with id {self._id} not found")
            else:
                # Create new note
                created_at_str = self.created_at.isoformat()
                cursor.execute('''
                    INSERT INTO notes (title, content, tags, start_time, end_time, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (self.title, self.content, tags_json, 
                     start_time_str, end_time_str, created_at_str, updated_at_str))
                
                self._id = cursor.lastrowid
            
            conn.commit()
            self.updated_at = datetime.fromisoformat(updated_at_str)
            logger.info(f"✅ Note saved successfully with ID: {self._id}")
            return self
            
        except Exception as e:
            error_msg = f"Error saving note: {e}"
            logger.error(error_msg)
            if conn:
                conn.rollback()
            raise Exception(error_msg)
        finally:
            if conn:
                conn.close()
    
    @classmethod
    def find_all(cls):
        """Get all notes, ordered by most recently updated"""
        try:
            conn = database.get_connection()
            if not conn:
                return []
                
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM notes ORDER BY updated_at DESC')
            rows = cursor.fetchall()
            conn.close()
            
            return [cls.from_dict(dict(row)) for row in rows]
            
        except Exception as e:
            logger.error(f"Error finding all notes: {e}")
            return []
    
    @classmethod
    def find_by_id(cls, note_id):
        """Find a note by ID"""
        try:
            conn = database.get_connection()
            if not conn:
                return None
                
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
            row = cursor.fetchone()
            conn.close()
            
            return cls.from_dict(dict(row)) if row else None
            
        except Exception as e:
            logger.error(f"Error finding note by ID: {e}")
            return None
    
    @classmethod
    def search(cls, query):
        """Search notes by title, content, or tags"""
        try:
            conn = database.get_connection()
            if not conn:
                return []
                
            cursor = conn.cursor()
            search_pattern = f'%{query}%'
            cursor.execute('''
                SELECT * FROM notes 
                WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?
                ORDER BY updated_at DESC
            ''', (search_pattern, search_pattern, search_pattern))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [cls.from_dict(dict(row)) for row in rows]
            
        except Exception as e:
            logger.error(f"Error searching notes: {e}")
            return []
    
    @classmethod
    def find_by_tag(cls, tag):
        """Find notes by specific tag"""
        try:
            conn = database.get_connection()
            if not conn:
                return []
                
            cursor = conn.cursor()
            # Search for tag in JSON array
            cursor.execute('''
                SELECT * FROM notes 
                WHERE tags LIKE ?
                ORDER BY updated_at DESC
            ''', (f'%"{tag}"%',))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [cls.from_dict(dict(row)) for row in rows]
            
        except Exception as e:
            logger.error(f"Error finding notes by tag: {e}")
            return []
    
    @classmethod
    def get_all_tags(cls):
        """Get all unique tags from all notes"""
        try:
            conn = database.get_connection()
            if not conn:
                return []
                
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT tags FROM notes WHERE tags IS NOT NULL AND tags != "[]"')
            rows = cursor.fetchall()
            conn.close()
            
            # Extract unique tags from JSON arrays
            all_tags = set()
            for row in rows:
                try:
                    tags = json.loads(row['tags'])
                    all_tags.update(tags)
                except:
                    continue
            
            return sorted(list(all_tags))
            
        except Exception as e:
            logger.error(f"Error getting all tags: {e}")
            return []
    
    def delete(self):
        """Delete the note from SQLite database"""
        try:
            if not self._id:
                return False
                
            conn = database.get_connection()
            if not conn:
                return False
                
            cursor = conn.cursor()
            cursor.execute('DELETE FROM notes WHERE id = ?', (self._id,))
            success = cursor.rowcount > 0
            conn.commit()
            conn.close()
            
            return success
            
        except Exception as e:
            logger.error(f"Error deleting note: {e}")
            return False
    
    @classmethod
    def from_dict(cls, data):
        """Create Note instance from dictionary"""
        if not data:
            return None
        
        # Parse tags from JSON string
        tags = []
        if data.get('tags'):
            try:
                tags = json.loads(data['tags'])
            except:
                tags = []
        
        # Parse datetime strings
        start_time = None
        end_time = None
        created_at = None
        updated_at = None
        
        if data.get('start_time'):
            try:
                start_time = datetime.fromisoformat(data['start_time'])
            except:
                pass
                
        if data.get('end_time'):
            try:
                end_time = datetime.fromisoformat(data['end_time'])
            except:
                pass
                
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
            title=data.get('title', ''),
            content=data.get('content', ''),
            tags=tags,
            start_time=start_time,
            end_time=end_time,
            created_at=created_at,
            updated_at=updated_at
        )
    
    def to_dict(self):
        """Convert Note instance to dictionary"""
        return {
            'id': self._id,
            'title': self.title,
            'content': self.content,
            'tags': self.tags,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Note {self.title}>'