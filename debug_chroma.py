from dotenv import load_dotenv
load_dotenv()

from chroma_client import get_collection
import json

col = get_collection("course_content")
data = col.get(include=["documents", "metadatas"])

print(json.dumps(data, indent=2))
