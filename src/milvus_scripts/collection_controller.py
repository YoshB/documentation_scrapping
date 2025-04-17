import os
from pymilvus import connections, Collection, utility
from typing import Any
from dotenv import load_dotenv

from ollama_scripts.embeddings import embed_text

load_dotenv()

# Usar las variables
milvus_host = os.getenv("MILVUS_HOST", "localhost")  # valor por defecto si no se encuentra
milvus_port = os.getenv("MILVUS_PORT", "19530")
milvus_user = os.getenv("MILVUS_USER")
mivlus_password = os.getenv("MILVUS_PASSWORD")
vector_dim = int(os.getenv("VECTOR_DIM", "384"))
col_name = os.getenv("COLLECTION_NAME", "library_docs")

# Conexión con autenticación
connections.connect(
        alias="default",
        host=milvus_host,
        port=milvus_port,
        user=milvus_user,
        password=mivlus_password,
        secure=False  # Cambia a True si estás usando HTTPS o autenticación segura
    )

def insert_in_milvus(collection_name:str, docs:list[dict[str, Any]]) -> None:
    collection = Collection(collection_name)

    vectors = embed_text([doc["content"] for doc in docs])

    entities = [
        [doc["library_name"] for doc in docs],
        [doc["description"] for doc in docs],
        [doc["content"][0:5040] for doc in docs], #Limitar la cantidad de caracteres a 5040
        vectors
    ]
    collection.insert(entities)
    print(f"✅ Insertadas {len(docs)} secciones en Milvus.")


def vector_search(collection_name:str, prompt:list[str], out_fields, limit:int=5) -> list[dict[str, Any]]:
    """
    Realiza una búsqueda vectorial en Milvus y devuelve los resultados.
    """
    collection = Collection(collection_name)

    vectors = embed_text(prompt)
    search_params = {
        "metric_type": "IP",
        "params": {"nprobe": 10}
    }
    results = collection.search(vectors, "vector", 
                                search_params, 
                                output_fields=out_fields,
                                limit=limit,
                                )
    
    # Procesar resultados
    docs = []
    for result in results:
        for hit in result:
            docs.append({x: hit.entity.get(x) for x in out_fields}) #Convertir a diccionario con las claves de outfields
    
    return docs[:limit]


