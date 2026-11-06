from langchain_core.tools import tool
from agent.memory.semantic import obtener_coleccion

@tool
def buscar_casos_similares(texto: str) -> list[dict]:
    """Recupera dos casos y dos políticas por similitud semántica con fuente citada."""
    if not texto.strip():
        return []
    resultados=[]
    for nombre,tipo in [('casos_previos','caso'),('politicas','politica')]:
        for d in obtener_coleccion(nombre).similarity_search(texto,k=2):
            resultados.append({'tipo':tipo,'texto':d.page_content,'meta':d.metadata})
    return resultados
