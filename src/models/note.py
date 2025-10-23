from datetime import datetime
from bson import ObjectId
from src.config.database import database

class Note:
    def __init__(self, title=None, content=None, tags=None, start_time=None, end_time=None, _id=None, created_at=None, updated_at=None):
        self._id = _id
        self.title = title
        self.content = content
        self.tags = tags or []  # List of tag strings
        self.start_time = start_time  # Start datetime
        self.end_time = end_time  # End datetime
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    @staticmethod
    def get_collection():
        """Get the notes collection from MongoDB"""
        return database.get_db().notes
    
    def save(self):
        """Save the note to MongoDB"""
        collection = self.get_collection()
        note_data = {
            'title': self.title,
            'content': self.content,
            'tags': self.tags,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'updated_at': datetime.utcnow()
        }
        
        if self._id:
            # Update existing note
            collection.update_one(
                {'_id': ObjectId(self._id)},
                {'$set': note_data}
            )
        else:
            # Create new note
            note_data['created_at'] = self.created_at
            result = collection.insert_one(note_data)
            self._id = str(result.inserted_id)
        
        self.updated_at = note_data['updated_at']
        return self
    
    @classmethod
    def find_all(cls):
        """Get all notes, ordered by most recently updated"""
        collection = cls.get_collection()
        notes = collection.find().sort('updated_at', -1)
        return [cls.from_dict(note) for note in notes]
    
    @classmethod
    def find_by_id(cls, note_id):
        """Find a note by ID"""
        try:
            collection = cls.get_collection()
            note = collection.find_one({'_id': ObjectId(note_id)})
            return cls.from_dict(note) if note else None
        except:
            return None
    
    @classmethod
    def search(cls, query):
        """Search notes by title, content, or tags"""
        collection = cls.get_collection()
        search_filter = {
            '$or': [
                {'title': {'$regex': query, '$options': 'i'}},
                {'content': {'$regex': query, '$options': 'i'}},
                {'tags': {'$regex': query, '$options': 'i'}}
            ]
        }
        notes = collection.find(search_filter).sort('updated_at', -1)
        return [cls.from_dict(note) for note in notes]
    
    @classmethod
    def find_by_tag(cls, tag):
        """Find notes by specific tag"""
        collection = cls.get_collection()
        notes = collection.find({'tags': tag}).sort('updated_at', -1)
        return [cls.from_dict(note) for note in notes]
    
    @classmethod
    def get_all_tags(cls):
        """Get all unique tags from all notes"""
        collection = cls.get_collection()
        pipeline = [
            {'$unwind': '$tags'},
            {'$group': {'_id': '$tags'}},
            {'$sort': {'_id': 1}}
        ]
        result = collection.aggregate(pipeline)
        return [item['_id'] for item in result]
    
    def delete(self):
        """Delete the note from MongoDB"""
        if self._id:
            collection = self.get_collection()
            collection.delete_one({'_id': ObjectId(self._id)})
            return True
        return False
    
    @classmethod
    def from_dict(cls, data):
        """Create Note instance from dictionary"""
        if not data:
            return None
        
        # Convert string datetime back to datetime objects if needed
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        
        if isinstance(start_time, str):
            try:
                start_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            except:
                start_time = None
                
        if isinstance(end_time, str):
            try:
                end_time = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            except:
                end_time = None
        
        return cls(
            _id=str(data['_id']),
            title=data.get('title', ''),
            content=data.get('content', ''),
            tags=data.get('tags', []),
            start_time=start_time,
            end_time=end_time,
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
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

