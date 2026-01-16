# rag_teacher.py
from chroma_client import get_collection
from openai import OpenAI
import os
import traceback

SYSTEM_BASE = """
You are an instructional design copilot for educators.

Rules:
- Guide the teacher using best-practice pedagogy
- Explain reasoning clearly and calmly
- Suggest improvements, alternatives, and checks
- NEVER overwrite or dictate final decisions
- Do NOT answer as a student
- Do NOT fabricate institutional policy
"""

MODE_CONFIG = {
    "design_guidance": {
        "collection": "pedagogy_frameworks",
        "system_suffix": (
            "Focus on curriculum design, learning outcomes, "
            "constructive alignment, and teaching strategies."
        )
    },
    "assessment_designer": {
        "collection": "assessment_frameworks",
        "system_suffix": (
            "Focus on assessment design, rubrics, CLO alignment, "
            "formative vs summative assessment, and validity."
        )
    }
}


def teacher_answer(req):
    try:
        print("▶ Teacher query received")
        print("Tenant:", req.tenant_id, "Course:", req.course_id)
        print("Mode:", req.mode)

        if req.mode not in MODE_CONFIG:
            return f"Unsupported teacher mode: {req.mode}"

        mode_cfg = MODE_CONFIG[req.mode]

        # Lazy init OpenAI (prevents startup crash)
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        collection_name = mode_cfg["collection"]
        system_prompt = SYSTEM_BASE + "\n\n" + mode_cfg["system_suffix"]

        print(f"▶ Using collection: {collection_name}")

        collection = get_collection(collection_name)

        print("▶ Querying scoped RAG DB...")
        res = collection.query(
            query_texts=[req.question],
            n_results=5
            # Future-safe: add tenant / course filter here
            # where={"tenant_id": req.tenant_id}
        )

        docs = res.get("documents", [[]])[0]
        docs = [d for d in docs if isinstance(d, str)]

        print("▶ Retrieved docs:", docs)

        if not docs:
            context = (
                "No specific reference material was found. "
                "Rely on general academic best practices."
            )
        else:
            context = "\n\n".join(docs)

        print("▶ Calling OpenAI (teacher copilot)...")

        out = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": (
                        f"Reference context:\n{context}\n\n"
                        f"Teacher question:\n{req.question}"
                    )
                }
            ],
            temperature=0.3
        )

        return out.choices[0].message.content.strip()

    except Exception:
        print("❌ TEACHER RAG ERROR")
        traceback.print_exc()
        return (
            "An internal error occurred while generating pedagogical guidance. "
            "Please check server logs."
        )

