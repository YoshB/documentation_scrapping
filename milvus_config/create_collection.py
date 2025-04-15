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
        FieldSchema(name="language", dtype=DataType.VARCHAR, max_length=64),
        FieldSchema(name="description", dtype=DataType.VARCHAR, max_length=1024),
        FieldSchema(name="code", dtype=DataType.VARCHAR, max_length=2048),
        FieldSchema(name="version", dtype=DataType.VARCHAR, max_length=64),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=vector_dim)
    ]

    # Define el schema
    schema = CollectionSchema(fields=fields, description="Collection to store library documentation parts")

    # Crea la colección
    collection_name = "library_docs"
    collection = Collection(name=collection_name, schema=schema)

    print(f"✅ Colección '{collection_name}' creada correctamente.")
except Exception as e:
    print(e)
    print(repr(e))
finally:
    # Desconectar
    connections.disconnect(alias="default")
    print("Desconectado de Milvus.")
