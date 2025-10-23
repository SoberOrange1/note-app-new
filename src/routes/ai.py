from flask import Blueprint, request, jsonify
import asyncio
from src.config.ai_client import ai_client
from src.models.note_sqlite import Note  # Switch to SQLite Note model

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/ai/summarize', methods=['POST'])
def summarize_note():
    """Generate a summary for note content"""
    try:
        data = request.get_json()
        content = data.get('content', '').strip()
        
        if not content:
            return jsonify({'error': 'Content is required'}), 400
        
        messages = [
            {
                "role": "user", 
                "content": f"Please provide a concise summary of the following text:\n\n{content}"
            }
        ]
        
        system_prompt = "You are a helpful assistant that creates clear, concise summaries of text content. Keep summaries under 100 words and focus on the main points."
        
        # Run async function in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            response = loop.run_until_complete(
                ai_client.chat_completion(
                    messages=messages,
                    system_prompt=system_prompt,
                    temperature=0.3,
                    max_tokens=200
                )
            )
        finally:
            loop.close()
        
        summary = ai_client.extract_content(response)
        return jsonify({'summary': summary})
        
    except Exception as e:
        return jsonify({'error': f'Failed to generate summary: {str(e)}'}), 500

@ai_bp.route('/ai/generate-tags', methods=['POST'])
def generate_tags():
    """Generate relevant tags for note content"""
    try:
        data = request.get_json()
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        
        if not title and not content:
            return jsonify({'error': 'Title or content is required'}), 400
        
        text_to_analyze = f"Title: {title}\n\nContent: {content}" if title else content
        
        messages = [
            {
                "role": "user",
                "content": f"Based on the following text, suggest 3-5 relevant tags that would help categorize and find this note. Return only the tags separated by commas, no explanations:\n\n{text_to_analyze}"
            }
        ]
        
        system_prompt = "You are a helpful assistant that generates relevant, concise tags for text content. Return only the tags separated by commas, with no additional text or explanations."
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            response = loop.run_until_complete(
                ai_client.chat_completion(
                    messages=messages,
                    system_prompt=system_prompt,
                    temperature=0.5,
                    max_tokens=100
                )
            )
        finally:
            loop.close()
        
        tags_text = ai_client.extract_content(response)
        
        # Parse tags from response
        if tags_text and not tags_text.startswith('Error:'):
            tags = [tag.strip() for tag in tags_text.split(',') if tag.strip()]
            tags = tags[:5]  # Limit to 5 tags
        else:
            tags = []
        
        return jsonify({'tags': tags})
        
    except Exception as e:
        return jsonify({'error': f'Failed to generate tags: {str(e)}'}), 500

@ai_bp.route('/ai/improve-content', methods=['POST'])
def improve_content():
    """Improve note content with AI suggestions"""
    try:
        data = request.get_json()
        content = data.get('content', '').strip()
        improvement_type = data.get('type', 'general')  # general, grammar, clarity, expand
        
        if not content:
            return jsonify({'error': 'Content is required'}), 400
        
        # Different prompts for different improvement types
        prompts = {
            'general': "Please improve the following text by making it clearer, more organized, and easier to read:",
            'grammar': "Please correct any grammar, spelling, and punctuation errors in the following text:",
            'clarity': "Please rewrite the following text to make it clearer and more concise:",
            'expand': "Please expand on the following text by adding more detail and explanation:"
        }
        
        prompt = prompts.get(improvement_type, prompts['general'])
        
        messages = [
            {
                "role": "user",
                "content": f"{prompt}\n\n{content}"
            }
        ]
        
        system_prompt = "You are a helpful writing assistant. Improve the given text while maintaining the original meaning and tone. Return only the improved text without explanations."
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            response = loop.run_until_complete(
                ai_client.chat_completion(
                    messages=messages,
                    system_prompt=system_prompt,
                    temperature=0.3,
                    max_tokens=1500
                )
            )
        finally:
            loop.close()
        
        improved_content = ai_client.extract_content(response)
        return jsonify({'improved_content': improved_content})
        
    except Exception as e:
        return jsonify({'error': f'Failed to improve content: {str(e)}'}), 500

@ai_bp.route('/ai/chat', methods=['POST'])
def chat_with_notes():
    """Chat about notes or get answers based on note content"""
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        note_id = data.get('note_id')  # Optional: chat about specific note
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        # If note_id provided, include note content in context
        context = ""
        if note_id:
            note = Note.find_by_id(note_id)
            if note:
                context = f"Note Title: {note.title}\nNote Content: {note.content}\n\n"
        
        messages = [
            {
                "role": "user",
                "content": f"{context}Question: {question}"
            }
        ]
        
        system_prompt = "You are a helpful assistant that can answer questions about notes and provide insights. Be concise and helpful in your responses."
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            response = loop.run_until_complete(
                ai_client.chat_completion(
                    messages=messages,
                    system_prompt=system_prompt,
                    temperature=0.7,
                    max_tokens=800
                )
            )
        finally:
            loop.close()
        
        answer = ai_client.extract_content(response)
        return jsonify({'answer': answer})
        
    except Exception as e:
        return jsonify({'error': f'Failed to process chat: {str(e)}'}), 500

@ai_bp.route('/ai/search-assist', methods=['POST'])
def search_assist():
    """Help users find notes by understanding natural language queries"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        # Get all notes for context
        all_notes = Note.find_all()
        
        if not all_notes:
            return jsonify({'suggestions': [], 'search_terms': []})
        
        # Prepare notes context (limit to titles and first 100 chars of content)
        notes_context = []
        for note in all_notes[:20]:  # Limit to first 20 notes to avoid token limits
            preview = note.content[:100] + "..." if len(note.content) > 100 else note.content
            notes_context.append(f"- {note.title}: {preview}")
        
        context = "\n".join(notes_context)
        
        messages = [
            {
                "role": "user",
                "content": f"Available notes:\n{context}\n\nUser search query: '{query}'\n\nBased on the available notes, suggest the most relevant search terms or note titles that match the user's query. Return as a JSON array of strings."
            }
        ]
        
        system_prompt = "You are a search assistant. Analyze the user's query and available notes to suggest relevant search terms. Return only a JSON array of suggested search terms, no explanations."
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            response = loop.run_until_complete(
                ai_client.chat_completion(
                    messages=messages,
                    system_prompt=system_prompt,
                    temperature=0.3,
                    max_tokens=300
                )
            )
        finally:
            loop.close()
        
        suggestions_text = ai_client.extract_content(response)
        
        # Try to parse JSON response
        try:
            import json
            suggestions = json.loads(suggestions_text)
            if not isinstance(suggestions, list):
                suggestions = [suggestions_text]
        except:
            # Fallback: split by common delimiters
            suggestions = [s.strip().strip('"\'') for s in suggestions_text.replace('\n', ',').split(',') if s.strip()]
        
        return jsonify({'suggestions': suggestions[:5]})  # Limit to 5 suggestions
        
    except Exception as e:
        return jsonify({'error': f'Failed to process search assistance: {str(e)}'}), 500

@ai_bp.route('/ai/smart-create', methods=['POST'])
def smart_create_note():
    """AI automatically parse input text and extract title, content, and time information"""
    try:
        data = request.get_json()
        input_text = data.get('text', '').strip()
        
        if not input_text:
            return jsonify({'error': 'Input text is required'}), 400
        
        # Get current date and time information
        from datetime import datetime, timedelta
        import calendar
        
        now = datetime.now()
        current_date = now.strftime('%Y-%m-%d')
        current_time = now.strftime('%H:%M')
        current_weekday = calendar.day_name[now.weekday()]
        current_month = calendar.month_name[now.month]
        
        # Create context with current date/time information
        date_context = f"""Current date and time information:
- Today is {current_weekday}, {current_month} {now.day}, {now.year}
- Current date: {current_date}
- Current time: {current_time}

Use this information to interpret relative time expressions like:
- "tomorrow" = {(now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)).strftime('%Y-%m-%d')}
- "next week" = week starting {(now + timedelta(days=7-now.weekday())).strftime('%Y-%m-%d')}
- "this weekend" = {(now + timedelta(days=5-now.weekday())).strftime('%Y-%m-%d')} or {(now + timedelta(days=6-now.weekday())).strftime('%Y-%m-%d')}
"""

        messages = [
            {
                "role": "user",
                "content": f"""{date_context}

Please analyze the following text and extract structured information for a note. 

Text to analyze: "{input_text}"

Extract and return ONLY a JSON object with these fields:
- title: A concise title (max 50 characters)
- content: The main content/body text
- start_time: Start datetime in ISO format (YYYY-MM-DDTHH:MM) if mentioned, null if not found
- end_time: End datetime in ISO format (YYYY-MM-DDTHH:MM) if mentioned, null if not found

Examples of time expressions to interpret:
- "tomorrow at 3pm" = {(now.replace(hour=15, minute=0, second=0, microsecond=0) + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')}
- "next Monday 9am to 5pm" = calculate the next Monday date
- "this Friday from 2:00 to 3:30" = calculate this Friday's date
- "December 25th 2024 from 10:00 to 12:00"

Return only the JSON object, no explanations."""
            }
        ]
        
        system_prompt = """You are an expert at parsing natural language text to extract structured note information. 
        Focus on identifying:
        1. A clear, concise title that summarizes the main topic
        2. The detailed content/description
        3. Any mentioned dates and times (convert to ISO format)
        
        Always return valid JSON format only."""
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            response = loop.run_until_complete(
                ai_client.chat_completion(
                    messages=messages,
                    system_prompt=system_prompt,
                    temperature=0.1,  # Low temperature for consistent parsing
                    max_tokens=500
                )
            )
        finally:
            loop.close()
        
        ai_response = ai_client.extract_content(response)
        
        # Parse the JSON response
        try:
            import json
            import re
            
            # Clean the response to extract JSON
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                parsed_data = json.loads(json_str)
            else:
                # Fallback parsing
                raise ValueError("No JSON found in response")
            
            # Validate and clean the parsed data
            result = {
                'title': str(parsed_data.get('title', 'Untitled')).strip()[:50],
                'content': str(parsed_data.get('content', input_text)).strip(),
                'start_time': parsed_data.get('start_time'),
                'end_time': parsed_data.get('end_time')
            }
            
            # Validate datetime formats
            from datetime import datetime
            for time_field in ['start_time', 'end_time']:
                if result[time_field]:
                    try:
                        # Try to parse the datetime to validate format
                        datetime.fromisoformat(result[time_field].replace('Z', '+00:00'))
                    except:
                        result[time_field] = None
            
            return jsonify(result)
            
        except Exception as parse_error:
            # Fallback: create basic structure
            return jsonify({
                'title': input_text[:50] + '...' if len(input_text) > 50 else input_text,
                'content': input_text,
                'start_time': None,
                'end_time': None
            })
        
    except Exception as e:
        return jsonify({'error': f'Failed to parse text: {str(e)}'}), 500

@ai_bp.route('/ai/translate', methods=['POST'])
def translate_note():
    """Translate note content to specified language"""
    try:
        data = request.get_json()
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        target_language = data.get('target_language', 'english').lower()
        
        if not title and not content:
            return jsonify({'error': 'Title or content is required for translation'}), 400
        
        # Language mapping
        language_map = {
            'english': 'English',
            'chinese': 'Chinese (Simplified)',
            'japanese': 'Japanese'
        }
        
        target_lang_name = language_map.get(target_language, 'English')
        
        # Prepare text to translate
        text_to_translate = ""
        if title:
            text_to_translate += f"Title: {title}\n\n"
        if content:
            text_to_translate += f"Content: {content}"
        
        messages = [
            {
                "role": "user",
                "content": f"""Please translate the following note to {target_lang_name}. 
                
Maintain the structure and formatting. Return the translation in JSON format with 'title' and 'content' fields.

Text to translate:
{text_to_translate}

Return only a JSON object like:
{{"title": "translated title", "content": "translated content"}}"""
            }
        ]
        
        system_prompt = f"You are a professional translator. Translate the given text accurately to {target_lang_name} while preserving the meaning, tone, and structure. Return only the JSON object with translated title and content."
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            response = loop.run_until_complete(
                ai_client.chat_completion(
                    messages=messages,
                    system_prompt=system_prompt,
                    temperature=0.3,  # Low temperature for accurate translation
                    max_tokens=2000
                )
            )
        finally:
            loop.close()
        
        ai_response = ai_client.extract_content(response)
        
        # Parse the JSON response
        try:
            import json
            import re
            
            # Clean the response to extract JSON
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                parsed_data = json.loads(json_str)
            else:
                # Fallback parsing
                raise ValueError("No JSON found in response")
            
            result = {
                'title': str(parsed_data.get('title', title)).strip(),
                'content': str(parsed_data.get('content', content)).strip(),
                'target_language': target_lang_name
            }
            
            return jsonify(result)
            
        except Exception as parse_error:
            # Fallback: return original text if parsing fails
            return jsonify({
                'title': title,
                'content': content,
                'target_language': target_lang_name,
                'error': 'Translation parsing failed, returned original text'
            })
        
    except Exception as e:
        return jsonify({'error': f'Failed to translate note: {str(e)}'}), 500