from chroma_client import get_collection

collection = get_collection("course_content")

collection.delete(
    where={
        "$and": [
            {"tenant_id": "imu_demo"},
            {"course_id": "101"}
        ]
    }
)

print("✅ Course index cleared")
