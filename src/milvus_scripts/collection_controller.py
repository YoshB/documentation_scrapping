import os
from pymilvus import connections, Collection
from typing import Any
from dotenv import load_dotenv

from ollama_scripts.embeddings import embed_text

load_dotenv()

# Configurar Milvus
connections.connect(
    alias="default",
    host=os.getenv("MILVUS_HOST"),
    port=os.getenv("MILVUS_PORT"),
    user=os.getenv("MILVUS_USER"),
    password=os.getenv("MILVUS_PASSWORD"),
    secure=False
)
collection = Collection("library_docs")

def insert_in_milvus(docs:dict[str:str|Any]):
    descriptions = [d["description"] for d in docs]
    vectors = embed_text(descriptions)
    
    entities = [
        [doc["library_name"] for doc in docs],
        [doc["language"] for doc in docs],
        [doc["description"] for doc in docs],
        [doc["code"] for doc in docs],
        [doc["version"] for doc in docs],
        vectors
    ]
    collection.insert(entities)
    print(f"✅ Insertadas {len(docs)} secciones en Milvus.")