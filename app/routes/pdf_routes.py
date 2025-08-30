from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import tempfile
from ..services.rag_service import create_session_from_pdf, answer_question, delete_session
from ..models.schemas import UploadResponse, AskResponse
from ..store.memory_store import vector_stores, session_activity

router = APIRouter()

@router.post("/upload-pdf", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    session_id = create_session_from_pdf(tmp_path)
    return {"session_id": session_id}

@router.post("/ask", response_model=AskResponse)
async def ask(session_id: str = Form(...), query: str = Form(...)):
    try:
        answer = answer_question(session_id, query)
        return {"answer": answer}
    except ValueError:
        raise HTTPException(status_code=404, detail="Session expired or not found.")

@router.post("/delete-session/{session_id}")
async def delete_session_route(session_id: str):
    delete_session(session_id)
    return {"deleted": True}

@router.get("/data")
async def get_vector_db():
    # Return session IDs and their vectors (as lists of floats)
    vector_db = {}
    for sid, store in vector_stores.items():
        if hasattr(store, 'index') and hasattr(store.index, 'reconstruct_n'):
            try:
                n = store.index.ntotal
                # Get all vectors as lists of floats
                vectors = [store.index.reconstruct(i).tolist() for i in range(n)]
                vector_db[sid] = vectors
            except Exception as e:
                vector_db[sid] = f"error: {str(e)}"
        else:
            vector_db[sid] = 'unknown'
    session_summary = {sid: ts.isoformat() for sid, ts in session_activity.items()}
    return {"vector_db": vector_db, "session_data": session_summary}