import os
from ollama import Client
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()


# Usar las variables
ollama_host = os.getenv("OLLAMA_API_URL", "http://localhost:11434")  # valor por defecto si no se encuentra
embeddings_model = os.getenv("EMBEDDINGS_MODEL", "all-minilm")

def embed_text(inputs:list[str]) -> list[list[float]]:
    """
    Embeds the input text using the specified model.
    Input: an array of strings to embed.
    Output: an array of arrays of floats, each representing the embedding of the corresponding input string.
    """
    
    client = Client(host=ollama_host)

    embed_text = client.embed(model=embeddings_model, input=inputs)
    return embed_text.embeddings




