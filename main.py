from fastapi import FastAPI, Depends
from schemas import ChatRequest, IndexRequest
from security import verify_key
from indexer import index_course
from rag_student import student_answer
from rag_teacher import teacher_answer
from fastapi import UploadFile, File, Form
from utils.pdf_loader import extract_text_from_pdf_bytes
from utils.chunker import chunk_text


app = FastAPI(
    title="XueDao AI Service",
    root_path="/ai"
)

CHAT_MODES = {
    "student_chat": {
        "roles": ["student"],
        "handler": "student"
    },
    "design_guidance": {
        "roles": ["teacher"],
        "handler": "teacher"
    },
    "assessment_designer": {
        "roles": ["teacher"],
        "handler": "teacher"
    }
}

@app.post("/chat", dependencies=[Depends(verify_key)])
def chat(req: ChatRequest):

    if req.mode not in CHAT_MODES:
        return {"error": f"Unsupported mode: {req.mode}"}

    mode_cfg = CHAT_MODES[req.mode]

    if req.role not in mode_cfg["roles"]:
        return {"error": f"Role '{req.role}' not allowed for mode '{req.mode}'"}

    if mode_cfg["handler"] == "student":
        return {"answer": student_answer(req)}

    elif mode_cfg["handler"] == "teacher":
        return {"answer": teacher_answer(req)}

    return {"error": "Invalid handler"}


@app.get("/modes", dependencies=[Depends(verify_key)])
def list_modes():
    return {
        "modes": [
            {
                "mode": mode,
                "roles": cfg["roles"]
            }
            for mode, cfg in CHAT_MODES.items()
        ]
    }


@app.post("/index", dependencies=[Depends(verify_key)])
def index_endpoint(req: IndexRequest):
    return index_course(req.items)

@app.post("/index/pdf", dependencies=[Depends(verify_key)])
async def index_pdf(
    file: UploadFile = File(...),
    tenant_id: str = Form(...),
    course_id: int = Form(...),
    module: str = Form(...),
    scope: str = Form(...),
    title: str = Form(...)
):
    pdf_bytes = await file.read()

    # 1️⃣ Extract text from PDF
    full_text = extract_text_from_pdf_bytes(pdf_bytes)

    if not full_text.strip():
        return {"error": "No extractable text found in PDF"}

    # 2️⃣ Chunk text
    chunks = chunk_text(full_text)

    # 3️⃣ Prepare items for existing indexer
    items = []
    for i, chunk in enumerate(chunks):
        items.append({
            "tenant_id": tenant_id,
            "course_id": course_id,
            "module": module,
            "scope": scope,
            "title": f"{title} (part {i+1})",
            "content": chunk,
            "source": "moodle_pdf"
        })

    # 4️⃣ Reuse existing index logic
    return index_course(items)
