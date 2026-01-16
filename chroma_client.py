# chroma_client.py
from dotenv import load_dotenv
load_dotenv("/var/www/xuedao-ai-service/.env")


import os
import chromadb
from chromadb.utils import embedding_functions

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DIR = os.path.join(BASE_DIR, "chroma")

_client = None


def get_client():
    global _client
    if _client is None:
        os.makedirs(CHROMA_DIR, exist_ok=True)

        _client = chromadb.PersistentClient(
            path=CHROMA_DIR
        )
    return _client


def get_collection(name: str):
    client = get_client()

    embedding_function = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-large"
    )

    return client.get_or_create_collection(
        name=name,
        embedding_function=embedding_function
    )
