"""Indexa secciones y cuatro casos empresariales; actualiza sin borrar carpetas."""
from langchain_chroma import Chroma
from langchain_core.documents import Document
from config.settings import DATA_DIR, CHROMA_DIR
from agent.memory.semantic import embeddings, obtener_coleccion

def indexar():
    secciones=(DATA_DIR/'politicas.md').read_text(encoding='utf-8').split('\n## ')[1:]
    politicas=[Document(page_content=s.strip(),metadata={'fuente':'politicas.md','seccion':f'S{i+1}'}) for i,s in enumerate(secciones)]
    textos=[
        'Incidente de mouse que no responde, cobertura vigente, se generó orden estándar P3.',
        'Servidor requiere repuesto de $250.000: la orden quedó bloqueada hasta aprobación de jefatura.',
        'Solicitante con cinco incidentes en 90 días: soporte nivel 2 investiga causa raíz.',
        'Impresora sin conexión con SLA excedido: escalamiento al coordinador de soporte.'
    ]
    casos=[Document(page_content=s,metadata={'fuente':'caso_previo','id':f'C{i+1}'}) for i,s in enumerate(textos)]
    for nombre,docs in [('politicas',politicas),('casos_previos',casos)]:
        db=Chroma(collection_name=nombre,embedding_function=embeddings(),persist_directory=str(CHROMA_DIR))
        db.add_documents(docs,ids=[f'{nombre}-{i}' for i in range(len(docs))])
    obtener_coleccion.cache_clear()
    print(f'Indexadas {len(politicas)} secciones y {len(casos)} casos previos.')

if __name__=='__main__':
    indexar()
