from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from .pdf_service import extract_text_from_pdf
from ..store.memory_store import vector_stores, session_activity
from datetime import datetime
import uuid

def create_session_from_pdf(file_path: str) -> str:
    text = extract_text_from_pdf(file_path)
    chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100).split_text(text)
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(chunks, embeddings)

    session_id = str(uuid.uuid4())
    vector_stores[session_id] = vector_store
    session_activity[session_id] = datetime.utcnow()
    return session_id

def answer_question(session_id: str, query: str) -> str:
    if session_id not in vector_stores:
        raise ValueError("Session not found.")
    session_activity[session_id] = datetime.utcnow()
    retriever = vector_stores[session_id].as_retriever(search_kwargs={"k": 5})
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.0)
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain.run(query)

def delete_session(session_id: str):
    vector_stores.pop(session_id, None)
    session_activity.pop(session_id, None)
