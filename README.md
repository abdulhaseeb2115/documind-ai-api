# DocuMind AI - Backend Server

FastAPI backend server for DocuMind AI, providing PDF processing and RAG-based question answering capabilities.

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API Key ([Get yours here](https://platform.openai.com/api-keys))

### Installation

1. **Create and activate a virtual environment:**

```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**

Create a `.env` file in the `server` directory:

```env
# Required: Your OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Frontend origin (default: http://localhost:3000)
FRONTEND_ORIGIN=http://localhost:3000

# Optional: Session TTL in minutes (default: 30)
SESSION_TTL_MINUTES=30
```

**⚠️ Important:** The `OPENAI_API_KEY` is **required** for the application to function. Without it, PDF processing and Q&A features will not work.

### Running the Server

```bash
# Make sure virtual environment is activated
uvicorn app.main:app --reload --port 8000
```

The server will be available at `http://localhost:8000`

- API Documentation: `http://localhost:8000/docs` (Swagger UI)
- Alternative Docs: `http://localhost:8000/redoc` (ReDoc)

## 📁 Project Structure

```
server/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration & environment variables
│   ├── routes/
│   │   └── pdf_routes.py    # API route handlers
│   ├── services/
│   │   ├── pdf_service.py   # PDF text extraction
│   │   └── rag_service.py   # RAG pipeline & Q&A logic
│   ├── models/
│   │   └── schemas.py       # Pydantic data models
│   ├── store/
│   │   └── memory_store.py # In-memory session storage
│   └── utils/
│       └── cleanup.py       # Session cleanup tasks
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create this)
└── README.md
```

## 🔌 API Endpoints

### 1. Upload PDF

Upload a PDF file to create a new session.

**Endpoint:** `POST /upload-pdf`

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (PDF file)

**Response:**
```json
{
  "session_id": "uuid-string"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/upload-pdf" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

### 2. Ask Question

Ask a question about the uploaded PDF.

**Endpoint:** `POST /ask`

**Request:**
- Content-Type: `application/x-www-form-urlencoded`
- Body:
  - `session_id`: Session ID from upload
  - `query`: Your question

**Response:**
```json
{
  "answer": "Answer text from the document"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "session_id=your-session-id" \
  -d "query=What is the main topic of this document?"
```

### 3. Delete Session

Delete a session and free up memory.

**Endpoint:** `POST /delete-session/{session_id}`

**Response:**
```json
{
  "deleted": true
}
```

### 4. Get Data (Debug)

Get vector database and session information (for debugging).

**Endpoint:** `GET /data`

**Response:**
```json
{
  "vector_db": {
    "session-id": [[vector arrays]]
  },
  "session_data": {
    "session-id": "2024-01-01T00:00:00"
  }
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | - | Your OpenAI API key (required for functionality) |
| `FRONTEND_ORIGIN` | No | `http://localhost:3000` | Frontend URL for CORS configuration |
| `SESSION_TTL_MINUTES` | No | `30` | Session timeout in minutes |

### CORS Configuration

The server is configured to allow requests from the frontend origin specified in `FRONTEND_ORIGIN`. Update this if your frontend runs on a different port or domain.

## 🏗️ Architecture

### RAG Pipeline

1. **PDF Upload** → Text extraction using PyPDF2
2. **Text Chunking** → RecursiveCharacterTextSplitter (1000 chars, 100 overlap)
3. **Embedding** → OpenAI embeddings (text-embedding-ada-002)
4. **Vector Store** → FAISS for similarity search
5. **Retrieval** → Top 5 most relevant chunks
6. **Generation** → GPT-3.5-turbo for answer generation

### Session Management

- Sessions are stored in-memory using dictionaries
- Each session has a unique UUID
- Sessions automatically expire after `SESSION_TTL_MINUTES`
- Background cleanup task removes expired sessions
- Vector stores are cleaned up when sessions expire

### Memory Store

- `vector_stores`: Dictionary mapping session_id → FAISS vector store
- `session_activity`: Dictionary mapping session_id → last activity timestamp

## 📦 Dependencies

### Core Dependencies

- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **pydantic** - Data validation
- **python-multipart** - File upload support

### AI/ML Dependencies

- **langchain** - LLM application framework
- **langchain-community** - Community integrations
- **langchain-openai** - OpenAI integration
- **langchain-text-splitters** - Text chunking utilities
- **faiss-cpu** - Vector similarity search

### PDF Processing

- **PyPDF2** - PDF text extraction

### Utilities

- **python-dotenv** - Environment variable management

## 🧪 Development

### Running in Development Mode

```bash
uvicorn app.main:app --reload --port 8000
```

The `--reload` flag enables auto-reload on code changes.

### Running in Production

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Testing API Endpoints

1. **Using Swagger UI:**
   - Navigate to `http://localhost:8000/docs`
   - Interactive API documentation with "Try it out" feature

2. **Using curl:**
   ```bash
   # Upload PDF
   curl -X POST "http://localhost:8000/upload-pdf" \
     -F "file=@test.pdf"
   
   # Ask question
   curl -X POST "http://localhost:8000/ask" \
     -d "session_id=your-session-id" \
     -d "query=Your question here"
   ```

3. **Using Python requests:**
   ```python
   import requests
   
   # Upload PDF
   with open('document.pdf', 'rb') as f:
       response = requests.post(
           'http://localhost:8000/upload-pdf',
           files={'file': f}
       )
   session_id = response.json()['session_id']
   
   # Ask question
   response = requests.post(
       'http://localhost:8000/ask',
       data={'session_id': session_id, 'query': 'What is this about?'}
   )
   print(response.json()['answer'])
   ```

## 🐛 Troubleshooting

### Common Issues

**1. `OPENAI_API_KEY is not set` warning**
- **Solution:** Create a `.env` file in the `server` directory and add your OpenAI API key
- **Check:** Ensure the key has no extra whitespace or newlines

**2. Import errors**
- **Solution:** Make sure virtual environment is activated and dependencies are installed:
  ```bash
  source venv/bin/activate
  pip install -r requirements.txt
  ```

**3. CORS errors**
- **Solution:** Check that `FRONTEND_ORIGIN` in `.env` matches your frontend URL
- **Check:** Ensure CORS middleware is properly configured in `main.py`

**4. Session not found errors**
- **Solution:** Sessions expire after 30 minutes (or `SESSION_TTL_MINUTES`). Upload a new PDF to create a new session

**5. PDF processing errors**
- **Solution:** Ensure the PDF is not corrupted and contains extractable text
- **Check:** Some PDFs with images only may not work without OCR

### Debugging

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check session data:
```bash
curl http://localhost:8000/data
```

## 🔒 Security Considerations

- **API Keys:** Never commit `.env` files or API keys to version control
- **CORS:** Configure `FRONTEND_ORIGIN` appropriately for production
- **File Uploads:** Currently accepts any PDF; consider adding file size limits
- **Sessions:** In-memory storage; consider persistent storage for production
- **Rate Limiting:** Consider adding rate limiting for production use

## 📝 Code Structure

### Main Application (`app/main.py`)

- FastAPI app initialization
- CORS middleware configuration
- Route registration
- Background cleanup task startup

### Routes (`app/routes/pdf_routes.py`)

- `/upload-pdf` - PDF upload handler
- `/ask` - Question answering handler
- `/delete-session/{session_id}` - Session deletion
- `/data` - Debug endpoint

### Services

**PDF Service (`app/services/pdf_service.py`)**
- Text extraction from PDF files

**RAG Service (`app/services/rag_service.py`)**
- Session creation from PDF
- Question answering using RAG
- Session deletion

### Models (`app/models/schemas.py`)

- Pydantic models for request/response validation
- `UploadResponse` - Upload endpoint response
- `AskResponse` - Ask endpoint response

## 🚀 Production Deployment

### Environment Setup

1. Set production environment variables
2. Use production-grade ASGI server (Gunicorn with Uvicorn workers)
3. Configure reverse proxy (Nginx)
4. Set up SSL/TLS certificates
5. Configure proper CORS origins

### Example Production Command

```bash
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)

## 🤝 Contributing

When contributing to the backend:

1. Follow PEP 8 style guidelines
2. Add type hints to functions
3. Write docstrings for modules and functions
4. Test API endpoints before submitting PR
5. Update this README if adding new features

---

**Note:** This backend is designed to work with the DocuMind AI frontend. Make sure both frontend and backend are running for full functionality.
