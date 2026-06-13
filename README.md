# DOC-MIND — RAG PDF Q&A with LangChain & GROQ

**Project:** A simple Retrieval-Augmented Generation (RAG) demo that lets users upload PDF documents, indexes them into a local Chroma store, and ask questions over the document content using LangChain + GROQ LLMs.

- **Backend:** FastAPI service that accepts PDF uploads, ingests documents into Chroma, and exposes a streaming query endpoint.
- **Frontend:** Vite + React TypeScript UI to upload PDFs and send user questions to the backend (served from `frontend/`).

**Key features**
- Upload PDF files (server-side validation: PDF only, max ~10MB).
- Chunking + embedding ingestion into a Chroma collection per-file.
- Streaming answers from GROQ-backed LLM via LangChain.
- Per-session chat history persisted in the backend.

**Repository layout**
- `backend/` — FastAPI application and ingestion/retrieval services.
  - `src/api/routes/upload.py` — POST `/upload/post-file` to upload PDFs.
  - `src/api/routes/query.py` — POST `/query` to ask questions (streaming text response).
  - `requirements.txt` — Python deps for the backend.
- `frontend/` — Vite + React TypeScript client (UI for upload and Q&A).

**Quickstart — Backend (Windows example)**
1. Create and activate a virtual environment inside `backend/` (if not present):

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Provide environment variables (create `backend/.env`):

```
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=sqlite:///./chroma_store/chroma.sqlite3
# optional overrides
# CHROMA_PATH=./chroma_store
# UPLOAD_DIR=./uploads
```

4. Run the backend (using `uvicorn`):

```powershell
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The backend exposes a health endpoint: `GET /health` (200 OK).

**Quickstart — Frontend**

1. From the repository root:

```bash
cd frontend
npm install
npm run dev
```

2. The frontend (Vite) typically runs at `http://localhost:5173` — this origin is allowed by the backend CORS settings.

**API usage examples**

- Upload a PDF (this creates a collection named `<filename>_col` and ingests chunks):

```bash
curl -X POST "http://localhost:8000/upload/post-file" -F "file=@/path/to/your.pdf"
```

Response example:

```json
{ "status": "success", "collection-name": "mydoc_col", "total-chunks": 123 }
```

- Ask a question (streaming text response):

POST to `/query` with JSON body:

```json
{
  "query": "What is the main purpose of the document?",
  "collection_name": "mydoc_col",
  "session_id": "session-123"
}
```



**Architecture & flow**
1. User uploads a PDF via `/upload/post-file`.
2. Backend saves the PDF to `UPLOAD_DIR` and calls the ingestor to chunk and embed text.
3. Embeddings are stored in a Chroma collection named after the file (filename + `_col`).
4. When the user asks a question, the retriever fetches top documents from the Chroma collection and the LLM (via LangChain + GROQ) produces a streaming answer using the retrieved context and saved conversation history.


