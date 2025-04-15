import os
from dotenv import load_dotenv
from pymilvus import connections, utility

# Cargar variables del entorno
load_dotenv()

# Datos del usuario root y del nuevo usuario
milvus_host = os.getenv("MILVUS_HOST", "localhost")
milvus_port = os.getenv("MILVUS_PORT", "19530")
root_old_pwd = os.getenv("MILVUS_ROOT_OLD_PASSWORD")
root_new_pwd = os.getenv("MILVUS_ROOT_NEW_PASSWORD")


def change_user_password(username:str, old_password:str, new_password:str):

    # 2. Cambiar contraseña de root
    utility.update_password(user=username, old_password=old_password, new_password=new_password)
    print(f"✅ Contraseña de {username} actualizada.")

    connections.disconnect(alias="default")

def create_user(username:str, password:str):

    # 3. Crear nuevo usuario
    utility.create_user(user=username, password=password)
    print(f"✅ Usuario '{username}' creado correctamente.")

# 4. (Opcional) Asignar rol al nuevo usuario
# utility.grant_role(user=new_user, role_name="readwrite")  # También existe "admin" o "read"


