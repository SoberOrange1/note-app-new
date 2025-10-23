import os
import sys
import logging
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.config.database_sqlite import database  # Switch to SQLite
from src.routes.user import user_bp
from src.routes.note import note_bp
from src.routes.ai import ai_bp

# Configure logging for production
if os.environ.get('FLASK_ENV') == 'production':
    logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Use environment variable for secret key, with fallback
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')

# Enable CORS for all routes
CORS(app)

# Add a health check endpoint for deployment monitoring
@app.route('/api/health')
def health_check():
    """Health check endpoint for deployment monitoring"""
    try:
        db_status = database.is_connected()
        return jsonify({
            'status': 'healthy' if db_status else 'database_disconnected',
            'database_connected': db_status,
            'database_type': 'SQLite',
            'environment': os.environ.get('FLASK_ENV', 'development')
        }), 200 if db_status else 503
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

# Initialize SQLite database with error handling
try:
    database.init_app(app)
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")
    # Continue running the app even if database fails to initialize

# register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(note_bp, url_prefix='/api')
app.register_blueprint(ai_bp, url_prefix='/api')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

# Global error handler for 500 errors
@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong on the server'
    }), 500

if __name__ == '__main__':
    # Use environment variables for host and port in production
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(host=host, port=port, debug=debug)
