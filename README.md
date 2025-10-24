# NoteTaker - Personal Note Management Application
### This is the ex2 of Shujun Ju

A modern, responsive web application for managing personal notes with a beautiful user interface and full CRUD functionality, now powered by **MongoDB Atlas** cloud database.

## 🌟 Features

- **Create Notes**: Add new notes with titles and rich content
- **Edit Notes**: Update existing notes with real-time editing
- **Delete Notes**: Remove notes you no longer need
- **Search Notes**: Find notes quickly by searching titles and content
- **Auto-save**: Notes are automatically saved as you type
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Modern UI**: Beautiful gradient design with smooth animations
- **Real-time Updates**: Instant feedback and updates
- **Cloud Storage**: Data stored securely in MongoDB Atlas

## 🚀 Live Demo

The application is deployed and accessible at: **https://3dhkilc88dkk.manus.space**

## 🛠 Technology Stack

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with gradients, animations, and responsive design
- **JavaScript (ES6+)**: Interactive functionality and API communication

### Backend
- **Python Flask**: Web framework for API endpoints
- **PyMongo & Flask-PyMongo**: MongoDB integration and ORM-like operations
- **Flask-CORS**: Cross-origin resource sharing support

### Database
- **MongoDB Atlas**: Cloud-hosted NoSQL database for scalable data persistence
- **Document-based storage**: Flexible schema for note and user data

## 📁 Project Structure

```
notetaking-app/
├── src/
│   ├── config/
│   │   └── database.py      # MongoDB Atlas connection setup
│   ├── models/
│   │   ├── user.py          # User model with MongoDB operations
│   │   └── note.py          # Note model with MongoDB operations
│   ├── routes/
│   │   ├── user.py          # User API endpoints
│   │   └── note.py          # Note API endpoints
│   ├── static/
│   │   ├── index.html       # Frontend application
│   │   └── favicon.ico      # Application icon
│   └── main.py              # Flask application entry point
├── venv/                    # Python virtual environment
├── requirements.txt         # Python dependencies (updated for MongoDB)
├── .env.example            # Environment configuration template
├── .gitignore              # Git ignore rules (includes .env)
└── README.md               # This file
```

## 🔧 Local Development Setup

### Prerequisites
- Python 3.11+
- pip (Python package manager)
- **MongoDB Atlas account** (free tier available)

### MongoDB Atlas Setup

1. **Create MongoDB Atlas Account**
   - Go to [MongoDB Atlas](https://www.mongodb.com/atlas)
   - Sign up for a free account
   - Create a new cluster (free M0 tier)

2. **Configure Database Access**
   - Create a database user with read/write permissions
   - Add your IP address to the IP whitelist (or use 0.0.0.0/0 for development)

3. **Get Connection String**
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string

### Installation Steps

1. **Clone or download the project**
   ```bash
   cd note-taking-app-updated-SoberOrange1
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   ```bash
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Environment Variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env file with your MongoDB Atlas connection string
   # Replace <username>, <password>, <cluster-name>, and <database-name>
   ```

6. **Run the application**
   ```bash
   python src/main.py
   ```

7. **Access the application**
   - Open your browser and go to `http://localhost:5001`

## 📡 API Endpoints

### Notes API
- `GET /api/notes` - Get all notes (sorted by most recent)
- `POST /api/notes` - Create a new note
- `GET /api/notes/<id>` - Get a specific note
- `PUT /api/notes/<id>` - Update a note
- `DELETE /api/notes/<id>` - Delete a note
- `GET /api/notes/search?q=<query>` - Search notes

### Users API
- `GET /api/users` - Get all users
- `POST /api/users` - Create a new user
- `GET /api/users/<id>` - Get a specific user
- `PUT /api/users/<id>` - Update a user
- `DELETE /api/users/<id>` - Delete a user

### Request/Response Format
```json
{
  "id": "507f1f77bcf86cd799439011",
  "title": "My Note Title",
  "content": "Note content here...",
  "created_at": "2025-01-08T10:30:00.000Z",
  "updated_at": "2025-01-08T11:15:30.000Z"
}
```

## 🎨 User Interface Features

### Sidebar
- **Search Box**: Real-time search through note titles and content
- **New Note Button**: Create new notes instantly
- **Notes List**: Scrollable list of all notes with previews
- **Note Previews**: Show title, content preview, and last modified date

### Editor Panel
- **Title Input**: Edit note titles
- **Content Textarea**: Rich text editing area
- **Save Button**: Manual save option (auto-save also available)
- **Delete Button**: Remove notes with confirmation
- **Real-time Updates**: Changes reflected immediately

### Design Elements
- **Gradient Background**: Beautiful purple gradient backdrop
- **Glass Morphism**: Semi-transparent panels with backdrop blur
- **Smooth Animations**: Hover effects and transitions
- **Responsive Layout**: Adapts to different screen sizes
- **Modern Typography**: Clean, readable font stack

## 🔒 Database Schema

### MongoDB Collections

#### Notes Collection
```javascript
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "title": "My Note Title",
  "content": "Note content here...",
  "created_at": ISODate("2025-01-08T10:30:00.000Z"),
  "updated_at": ISODate("2025-01-08T11:15:30.000Z")
}
```

#### Users Collection
```javascript
{
  "_id": ObjectId("507f1f77bcf86cd799439012"),
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": ISODate("2025-01-08T09:00:00.000Z"),
  "updated_at": ISODate("2025-01-08T09:00:00.000Z")
}
```

## 🚀 Deployment

### Environment Variables
Set these in your production environment:
```bash
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/database
FLASK_ENV=production
SECRET_KEY=your-production-secret-key
```

### MongoDB Atlas Benefits
- **Automatic scaling**: Handles traffic spikes automatically
- **Built-in security**: Encryption, authentication, and authorization
- **Global clusters**: Deploy close to your users
- **Automated backups**: Point-in-time recovery
- **Real-time monitoring**: Performance insights and alerts

## 🔧 Configuration

### Required Environment Variables
- `MONGODB_URI`: Your MongoDB Atlas connection string
- `FLASK_ENV`: Set to `development` or `production`
- `SECRET_KEY`: Flask secret key for sessions

### MongoDB Features Used
- **Document storage**: Flexible schema for notes and users
- **Indexing**: Automatic indexing on `_id` fields
- **Text search**: MongoDB's built-in text search capabilities
- **Aggregation**: For complex queries and data analysis

## 📱 Browser Compatibility

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with your MongoDB Atlas instance
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues or questions:
1. Check the browser console for error messages
2. Verify MongoDB Atlas connection string is correct
3. Ensure your IP is whitelisted in MongoDB Atlas
4. Check that the Flask server is running
5. Verify all dependencies are installed

### Common MongoDB Atlas Issues
- **Connection timeout**: Check IP whitelist settings
- **Authentication failed**: Verify username/password in connection string
- **Database not found**: Ensure database name is correct in URI

## 🎯 Future Enhancements

Potential improvements for future versions:
- **User authentication**: JWT-based authentication system
- **Note sharing**: Share notes between users
- **Categories and tags**: Organize notes with metadata
- **Rich text formatting**: WYSIWYG editor integration
- **File attachments**: Store files in MongoDB GridFS
- **Full-text search**: Advanced search with MongoDB Atlas Search
- **Real-time collaboration**: WebSocket integration
- **Mobile app**: React Native or Flutter app
- **Export functionality**: PDF, Markdown, JSON export
- **Dark/light theme**: User preference storage
- **Offline support**: Progressive Web App capabilities

## 🔄 Migration from SQLite

This application has been migrated from SQLite to MongoDB Atlas for:
- **Better scalability**: Handle more concurrent users
- **Cloud reliability**: No local database file management
- **Advanced features**: Full-text search, aggregation pipelines
- **Global availability**: Access from anywhere
- **Automatic backups**: Built-in data protection

---

**Built with ❤️ using Flask, MongoDB Atlas, and modern web technologies**

