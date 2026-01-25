from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


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


class ContentScope(str, Enum):
    course_content = "course_content"
    reading_material = "reading_material"
    supplementary_material = "supplementary_material"
    case_study = "case_study"
    faq = "faq"

    hidden_material = "hidden_material"
    teaching_notes = "teaching_notes"
    design_guidance = "design_guidance"
    grading_guidance = "grading_guidance"

    assessment_reference = "assessment_reference"
    question_bank = "question_bank"
    rubric = "rubric"
    model_answer = "model_answer"
    exam_blueprint = "exam_blueprint"

    admin_only = "admin_only"
    policy = "policy"
    compliance = "compliance"
