from functools import lru_cache
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from config.settings import CHROMA_DIR

@lru_cache(maxsize=1)
def embeddings():
    return HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
        model_kwargs={'device':'cpu'}, encode_kwargs={'normalize_embeddings':True})

@lru_cache(maxsize=2)
def obtener_coleccion(nombre):
    if not (CHROMA_DIR / 'chroma.sqlite3').exists():
        raise RuntimeError('Primero ejecuta python -m scripts.index_politicas')
    return Chroma(collection_name=nombre,embedding_function=embeddings(),persist_directory=str(CHROMA_DIR))
