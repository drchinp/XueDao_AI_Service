import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from chroma_client import get_collection

col = get_collection("course_content")

res = col.get()

print("Total documents:", len(res["documents"]))
print("\n=== SAMPLE METADATA (first 10) ===\n")

for m in res["metadatas"][:10]:
    print(m)
