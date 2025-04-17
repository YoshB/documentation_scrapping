from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection

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
    # Conexión con autenticación
    connections.connect(
        alias="default",
        host=milvus_host,
        port=milvus_port,
        user=milvus_user,
        password=mivlus_password,
        secure=False  # Cambia a True si estás usando HTTPS o autenticación segura
    )

    # Define los campos
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="library_name", dtype=DataType.VARCHAR, max_length=256),
        FieldSchema(name="description", dtype=DataType.VARCHAR, max_length=1024),
        FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=5048),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=vector_dim)
    ]

    # Define el schema
    schema = CollectionSchema(fields=fields, description="Collection to store library documentation parts")

    # Crea la colección
    collection_name = col_name
    collection = Collection(name=collection_name, schema=schema)

    print(f"✅ Colección '{collection_name}' creada correctamente.")
    # 3. Crear índice sobre el campo 'embedding'
    index_params = {
        "metric_type": "IP",  # 'IP' para cosine similarity, 'L2' para Euclidean, 'COSINE' en Milvus 2.4+
        "index_type": "IVF_FLAT",  # Puedes usar HNSW, IVF_FLAT, IVF_SQ8, etc.
        "params": {"nlist": 20}  # nlist es número de clusters
    }

    collection.create_index(
        field_name="vector",
        index_params=index_params
    )

    # 4. (Opcional) Persistir los cambios en el índice
    collection.flush()
    # 5. Ahora puedes cargar la colección a memoria
    collection.load()

    print("¡Índice creado y colección cargada!")

except Exception as e:
    print(e)
    print(repr(e))
finally:
    # Desconectar
    connections.disconnect(alias="default")
    print("Desconectado de Milvus.")
