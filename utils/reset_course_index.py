import sys
import os

# Add project root to PYTHONPATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from chroma_client import get_collection


def reset_course():
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


if __name__ == "__main__":
    reset_course()
