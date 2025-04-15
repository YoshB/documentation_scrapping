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

def split_markdown_by_subsections(md_text):
    sections = defaultdict(dict)
    current_title = None
    current_subtitle = None
    buffer = []

    lines = md_text.splitlines()

    for line in lines:
        if line.startswith('# '):  # Título principal
            if current_subtitle and current_title:
                sections[current_title][current_subtitle] = '\n'.join(buffer).strip()
                buffer = []
            current_title = line[2:].strip()
            current_subtitle = None
        elif line.startswith('## '):  # Subtítulo
            if current_subtitle and current_title:
                sections[current_title][current_subtitle] = '\n'.join(buffer).strip()
                buffer = []
            current_subtitle = line[3:].strip()
        else:
            buffer.append(line)

    # Guardar la última sección al final
    if current_subtitle and current_title:
        sections[current_title][current_subtitle] = '\n'.join(buffer).strip()

    return sections


def main():
    url = scrap_url
    md = fetch_md_raw(url)
    docs = split_markdown_by_subsections(md)
    print(docs['Horizontal Bar Chart'])

    #insert_in_milvus(docs)

main()