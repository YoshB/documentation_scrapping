import os
import requests
from dotenv import load_dotenv

from milvus_scripts.collection_controller import insert_in_milvus

# Cargar entorno
load_dotenv()

col_name = os.getenv("COLLECTION_NAME", "library_docs")

# --- FUNCIONES ---

def get_markdown_files():
    GITHUB_API_URL = os.getenv("GITHUB_API_URL", "")
    response = requests.get(GITHUB_API_URL)
    response.raise_for_status()
    files_info = response.json()

    md_files = [file['name'] for file in files_info if file['name'].endswith('.md')]
    return md_files

def download_markdown_file(filename):
    RAW_BASE_URL = os.getenv("RAW_BASE_URL", "")
    url = RAW_BASE_URL + filename
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def download_all_md_files():
    md_files = get_markdown_files()
    md_contents = []
    for md_file in md_files:
        content = download_markdown_file(md_file)
        md_contents.append(content)
    return md_contents



def parse_markdown_to_dict(md_text: str, library_name:str) -> dict:
    """
    Parsea un archivo markdown en un diccionario con 'description' y 'content'.

    'description': título (primer encabezado #) + primer párrafo
    'content': el resto del contenido
    """
    lines = md_text.strip().splitlines()

    # Asegurarse de que empieza con un título
    if not lines or not lines[0].startswith("# "):
        raise ValueError("El archivo markdown debe comenzar con un título usando '# '")

    title = lines[0]
    
    # Buscar el primer párrafo (primer bloque de texto no vacío después del título)
    description_lines = [title]
    rest_lines = []
    found_paragraph = False

    for line in lines[1:]:
        if not found_paragraph:
            if line.strip() == "":
                continue
            description_lines.append(line)
            found_paragraph = True
        else:
            rest_lines.append(line)
    dict = {
        "library_name": library_name,  # Eliminar '# '
        "description": "\n".join(description_lines).strip(),
        "content": "\n".join(rest_lines).strip()  # Limitar a 5040 caracteres
    }

    return dict



def main():
    md = download_all_md_files()
    md_list = []
    for md_file in md:
        md_list.append(parse_markdown_to_dict(md_file, library_name="chart.js"))

    #docs = parse_markdown_to_dict(md)
    #print("description:", docs["description"])

    insert_in_milvus(col_name, md_list)

main()