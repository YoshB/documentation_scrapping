import os
import requests
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from ollama_scripts.embeddings import embed_text

# Cargar entorno
load_dotenv()

scrap_url = os.getenv("SCRAP_URL", "https://www.chartjs.org/docs/latest/")

# --- FUNCIONES ---

def fetch_md_raw(url):
    res = requests.get(url)
    res.raise_for_status()
    return res.text


from collections import defaultdict

def parse_markdown_to_dict(md_text: str) -> dict:
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

    return {
        "description": "\n".join(description_lines).strip(),
        "content": "\n".join(rest_lines).strip()
    }



def main():
    url = scrap_url
    md = fetch_md_raw(url)
    print(md)
    docs = parse_markdown_to_dict(md)
    print(docs)

    #insert_in_milvus(docs)

main()