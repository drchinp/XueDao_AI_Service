from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel):
    tenant_id: str
    course_id: int
    role: str
    mode: str
    question: str
    module: Optional[str] = None   # NEW


class CourseChunk(BaseModel):
    tenant_id: str
    course_id: int
    module: str
    scope: str          # ✅ REQUIRED for mode-based retrieval
    title: str
    content: str


class IndexRequest(BaseModel):
    items: List[CourseChunk]