import os
from dotenv import load_dotenv

ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(ENV_PATH)

print("🔥 AI_SERVICE_KEY loaded:", os.getenv("AI_SERVICE_KEY"))

from fastapi import FastAPI


from fastapi import FastAPI, Depends
from schemas import ChatRequest
from security import verify_key
from schemas import IndexRequest
from indexer import index_course
from rag_student import student_answer
from rag_teacher import teacher_answer
from fastapi import Header, HTTPException

API_KEY = os.getenv("XUEDAO_API_KEY")

if not API_KEY:
    raise RuntimeError("XUEDAO_API_KEY not set in environment")

def verify_api_key(x_api_key: str = Header(None)):
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Server misconfiguration: API key not set"
        )
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )


app = FastAPI(
    title="Moodle AI Service",
    root_path="/ai"
)
@app.post("/chat", dependencies=[Depends(verify_api_key)])
def chat(req: ChatRequest):
    if req.role == "student":
        return {"answer": student_answer(req)}
    elif req.role == "teacher":
        return {"answer": teacher_answer(req)}
    return {"error": "Invalid role"}


@app.post("/index", dependencies=[Depends(verify_api_key)])
def index_endpoint(req: IndexRequest):
    return index_course(req.items)





