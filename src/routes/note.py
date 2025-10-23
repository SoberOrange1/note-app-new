from flask import Blueprint, jsonify, request
from datetime import datetime
from src.models.note_sqlite import Note  # Switch to SQLite Note model
import logging

logger = logging.getLogger(__name__)

note_bp = Blueprint('note', __name__)

@note_bp.route('/notes', methods=['GET'])
def get_notes():
    """Get all notes, ordered by most recently updated"""
    try:
        notes = Note.find_all()
        return jsonify([note.to_dict() for note in notes])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes', methods=['POST'])
def create_note():
    """Create a new note"""
    try:
        data = request.json
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({'error': 'Title and content are required'}), 400
        
        # Parse datetime fields if provided
        start_time = None
        end_time = None
        
        if data.get('start_time'):
            try:
                start_time = datetime.fromisoformat(data['start_time'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'error': 'Invalid start_time format'}), 400
                
        if data.get('end_time'):
            try:
                end_time = datetime.fromisoformat(data['end_time'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'error': 'Invalid end_time format'}), 400
        
        # Validate time range
        if start_time and end_time and start_time >= end_time:
            return jsonify({'error': 'Start time must be before end time'}), 400
        
        note = Note(
            title=data['title'],
            content=data['content'],
            tags=data.get('tags', []),
            start_time=start_time,
            end_time=end_time
        )
        note.save()
        return jsonify(note.to_dict()), 201
    except Exception as e:
        error_message = str(e)
        logger.error(f"Error creating note: {error_message}")
        
        # Check if it's a database connection error
        if "Database connection not available" in error_message or "Database not connected" in error_message:
            return jsonify({
                'error': 'Database connection failed',
                'message': 'Unable to connect to the database. Please try again later.',
                'details': error_message
            }), 503
        
        return jsonify({
            'error': 'Failed to create note',
            'message': error_message
        }), 500

@note_bp.route('/notes/<note_id>', methods=['GET'])
def get_note(note_id):
    """Get a specific note by ID"""
    try:
        note = Note.find_by_id(note_id)
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        return jsonify(note.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<note_id>', methods=['PUT'])
def update_note(note_id):
    """Update a specific note"""
    try:
        note = Note.find_by_id(note_id)
        if not note:
            return jsonify({'error': 'Note not found'}), 404
            
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        note.title = data.get('title', note.title)
        note.content = data.get('content', note.content)
        note.tags = data.get('tags', note.tags)
        
        # Parse datetime fields if provided
        if 'start_time' in data:
            if data['start_time']:
                try:
                    note.start_time = datetime.fromisoformat(data['start_time'].replace('Z', '+00:00'))
                except ValueError:
                    return jsonify({'error': 'Invalid start_time format'}), 400
            else:
                note.start_time = None
                
        if 'end_time' in data:
            if data['end_time']:
                try:
                    note.end_time = datetime.fromisoformat(data['end_time'].replace('Z', '+00:00'))
                except ValueError:
                    return jsonify({'error': 'Invalid end_time format'}), 400
            else:
                note.end_time = None
        
        # Validate time range
        if note.start_time and note.end_time and note.start_time >= note.end_time:
            return jsonify({'error': 'Start time must be before end time'}), 400
        
        note.save()
        return jsonify(note.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a specific note"""
    try:
        note = Note.find_by_id(note_id)
        if not note:
            return jsonify({'error': 'Note not found'}), 404
            
        note.delete()
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/search', methods=['GET'])
def search_notes():
    """Search notes by title, content, or tags"""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify([])
        
        notes = Note.search(query)
        return jsonify([note.to_dict() for note in notes])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/tags', methods=['GET'])
def get_all_tags():
    """Get all unique tags from all notes"""
    try:
        tags = Note.get_all_tags()
        return jsonify(tags)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/tags/<tag>', methods=['GET'])
def get_notes_by_tag(tag):
    """Get all notes with a specific tag"""
    try:
        notes = Note.find_by_tag(tag)
        return jsonify([note.to_dict() for note in notes])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

