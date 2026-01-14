# rag_student.py
from chroma_client import get_collection
from openai import OpenAI
import traceback
import os

def student_answer(req):
    try:
        print("▶ Student query received")
        print("Tenant:", req.tenant_id, "Course:", req.course_id)

        collection = get_collection("course_content")

        print("▶ Querying ChromaDB...")
        res = collection.query(
            query_texts=[req.question],
            n_results=5,
            where={
                "$and": [
                    {"tenant_id": req.tenant_id},
                    {"course_id": req.course_id}
                ]
            }
        )

        docs = res.get("documents", [[]])[0]
        docs = [d for d in docs if isinstance(d, str)]

        print("▶ Retrieved docs:", docs)

        if not docs:
            return "This topic is not covered in the course materials."

        context = "\n\n".join(docs)

        print("▶ Calling OpenAI...")
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Answer using course content only."},
                {"role": "user", "content": f"{context}\n\nQuestion: {req.question}"}
            ],
            temperature=0.2
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("❌ STUDENT RAG ERROR")
        traceback.print_exc()
        return "Internal error occurred. Check server logs."
