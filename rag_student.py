# rag_student.py
from chroma_client import get_collection
from openai import OpenAI
import traceback
import os

def student_answer(req):
    try:
        print("▶ Student query received")
        print("Tenant:", req.tenant_id, "Course:", req.course_id)
        print("Module:", getattr(req, "module", None))

        collection = get_collection("course_content")

        print("▶ Querying ChromaDB (strict)...")

        # 🔒 Strict filters (course-safe)
        strict_filters = [
            {"tenant_id": str(req.tenant_id)},
            {"course_id": str(req.course_id)},   # ⚠️ must be str
            {"scope": "course_content"}
        ]

        if getattr(req, "module", None):
            strict_filters.append({"module": str(req.module)})

        # 1️⃣ STRICT query
        res = collection.query(
            query_texts=[req.question],
            n_results=5,
            where={"$and": strict_filters}
        )

        print("▶ METADATAS (strict):", res.get("metadatas"))

        docs = res.get("documents", [[]])[0]
        docs = [d for d in docs if isinstance(d, str)]

        print("▶ Strict docs:", docs)

        # 2️⃣ Fallback: relax course_id (still tenant + scope safe)
        if not docs:
            print("▶ Fallback query (relax course_id)")

            fallback_filters = [
                {"tenant_id": str(req.tenant_id)},
                {"scope": "course_content"}
            ]

            if getattr(req, "module", None):
                fallback_filters.append({"module": str(req.module)})

            res = collection.query(
                query_texts=[req.question],
                n_results=5,
                where={"$and": fallback_filters}
            )

            print("▶ METADATAS (fallback):", res.get("metadatas"))

            docs = res.get("documents", [[]])[0]
            docs = [d for d in docs if isinstance(d, str)]

            print("▶ Fallback docs:", docs)

        if not docs:
            return "This topic is not covered in the course materials."

        context = "\n\n".join(docs)

        print("▶ Calling OpenAI...")
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Answer using course content only. Do not add external knowledge."
                },
                {
                    "role": "user",
                    "content": f"{context}\n\nQuestion: {req.question}"
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Internal error: {str(e)}"


