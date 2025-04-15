from users_controller import create_user, change_user_password
import os
from dotenv import load_dotenv
from pymilvus import connections

# Cargar variables del entorno
load_dotenv()

# Datos del usuario root y del nuevo usuario
milvus_host = os.getenv("MILVUS_HOST", "localhost")
milvus_port = os.getenv("MILVUS_PORT", "19530")
root_new_pwd = os.getenv("MILVUS_ROOT_PASSWORD")
new_user = os.getenv("MILVUS_USER")
new_user_pwd = os.getenv("MILVUS_PASSWORD")


try:
    # 1. Conectar como root con la contraseña original
    connections.connect(
            alias="default",
            host=milvus_host,
            port=milvus_port,
            user='root',
            password='Milvus',
            secure=False
        )
    print(f"Conectando a Milvus en {milvus_host}:{milvus_port} como root")

    # 2. Cambiar contraseña de root
    change_user_password(username='root', old_password='Milvus', new_password=root_new_pwd)
    print("✅ Contraseña de root cambiada correctamente.")
    # 2.5 Conectar de nuevo con la nueva contraseña
    connections.connect(
            alias="default",
            host=milvus_host,
            port=milvus_port,
            user='root',
            password=root_new_pwd,
            secure=False
        )
    # 3. Crear nuevo usuario
    create_user(username=new_user, password=new_user_pwd)
except Exception as e:
    print(e)
    print(repr(e))
finally:    
    connections.disconnect(alias="default")
    print("Desconectado de Milvus.")