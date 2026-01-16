from fastapi import FastAPI, Depends
from schemas import ChatRequest, IndexRequest
from security import verify_key
from indexer import index_course
from rag_student import student_answer
from rag_teacher import teacher_answer

app = FastAPI(
    title="XueDao AI Service",
    root_path="/ai"
)

@app.post("/chat", dependencies=[Depends(verify_key)])
def chat(req: ChatRequest):
    if req.role == "student":
        return {"answer": student_answer(req)}
    elif req.role == "teacher":
        return {"answer": teacher_answer(req)}
    return {"error": "Invalid role"}

@app.post("/index", dependencies=[Depends(verify_key)])
def index_endpoint(req: IndexRequest):
    return index_course(req.items)
