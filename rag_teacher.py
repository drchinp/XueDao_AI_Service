# rag_teacher.py
from chroma_client import get_collection
from openai import OpenAI
import os
import traceback

SYSTEM = """
You are an instructional design copilot for educators.

Rules:
- Guide the teacher using best-practice pedagogy
- Explain reasoning clearly and calmly
- Suggest improvements, alternatives, and checks
- NEVER overwrite or dictate final decisions
- Do NOT answer as a student
- Do NOT fabricate institutional policy
"""

def teacher_answer(req):
    try:
        print("▶ Teacher query received")
        print("Tenant:", req.tenant_id, "Course:", req.course_id)
        print("Mode:", req.mode)

        # Lazy init OpenAI (prevents startup crash)
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        pedagogy = get_collection("pedagogy_frameworks")

        print("▶ Querying pedagogy framework DB...")
        res = pedagogy.query(
            query_texts=[req.question],
            n_results=5
            # NOTE: no `where` yet; add later if tenant-scoped
        )

        docs = res.get("documents", [[]])[0]
        docs = [d for d in docs if isinstance(d, str)]

        print("▶ Retrieved pedagogy docs:", docs)

        if not docs:
            context = (
                "No specific pedagogy framework text was found. "
                "Rely on general instructional design principles."
            )
        else:
            context = "\n\n".join(docs)

        print("▶ Calling OpenAI (teacher copilot)...")

        out = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": SYSTEM},
                {
                    "role": "user",
                    "content": (
                        f"Pedagogical context:\n{context}\n\n"
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

