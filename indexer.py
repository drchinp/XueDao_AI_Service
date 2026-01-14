from chroma_client import get_collection

def index_course(items):
    collection = get_collection("course_content")

    documents = []
    metadatas = []
    ids = []

    for idx, item in enumerate(items):
        documents.append(item.content)

        metadatas.append({
            "tenant_id": str(item.tenant_id),
            "course_id": str(item.course_id),   # keep as string
            "module": item.module,
            "title": item.title
        })

        ids.append(
            f"{item.tenant_id}_{item.course_id}_{idx}"
        )

    # 🔍 DEBUG VISIBILITY (critical)
    print("▶ Indexing documents:", documents)
    print("▶ Metadatas:", metadatas)
    print("▶ IDs:", ids)

    # ✅ Use upsert instead of add (forces embedding & persistence)
    collection.upsert(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    # 🔍 VERIFY immediately (this is the key)
    verify = collection.get(ids=ids, include=["documents"])
    print("✅ Verified stored docs:", verify["documents"])

    return {"indexed_chunks": len(documents)}
