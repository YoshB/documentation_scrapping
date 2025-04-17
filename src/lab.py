from pymilvus import utility, connections, Collection
from milvus_scripts.collection_controller import vector_search

import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Usar las variables
milvus_host = os.getenv("MILVUS_HOST", "localhost")  # valor por defecto si no se encuentra
milvus_port = os.getenv("MILVUS_PORT", "19530")
milvus_user = os.getenv("MILVUS_USER")
mivlus_password = os.getenv("MILVUS_PASSWORD")
vector_dim = int(os.getenv("VECTOR_DIM", "384"))
col_name = os.getenv("COLLECTION_NAME", "library_docs")

print(f"Conectando a Milvus en {milvus_host}:{milvus_port} con vectores de dimensión {vector_dim}")

try:

    col = Collection(col_name)


    out_fields = ["description"]
    res = vector_search(col_name, ["quiero una grafica que muestre los porcentajes de unos pocos elementos"], out_fields=out_fields, limit=2)
    print(res)

except Exception as e:
    print(e)
    print(repr(e))
    # Desconectar   
 





