import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from chroma_client import get_client

client = get_client()

print("📦 Existing Chroma collections:")
for col in client.list_collections():
    print("-", col.name)
