from pydantic import BaseModel

class UploadResponse(BaseModel):
    session_id: str

class AskResponse(BaseModel):
    answer: str
