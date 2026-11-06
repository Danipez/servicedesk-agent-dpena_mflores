import pytest
from agent.core import procesar_solicitud
from agent.memory.short_term import crear_memoria_corto_plazo
from agent.memory.long_term import obtener_historial
from agent.storage import conectar

@pytest.mark.parametrize('ticket,accion,orden',[
    ('INC-001','resolver_estandar',True),
    ('INC-015','escalar',False),
    ('INC-022','solicitar_aprobacion',False),
    ('INC-030','escalar_recurrencia',False),
    ('INC-035','solicitar_info',False),
    ('INC-040','escalar',False),
])
def test_flujo(ticket,accion,orden):
    r=procesar_solicitud(ticket,usar_rag=False)
    assert r['ok'] and r['accion']==accion
    assert ('orden' in r)==orden
    assert r['notificacion']['ok']
    assert len(obtener_historial(r['ticket']['solicitante_id']))==1

def test_cambio_por_memoria():
    assert procesar_solicitud('INC-001',usar_rag=False)['accion']=='resolver_estandar'
    segunda=procesar_solicitud('INC-001',usar_rag=False)
    assert segunda['accion']=='resolver_preferente'
    assert len(segunda['ticket']['historial_solicitante'])==1
    with conectar() as c:
        assert c.execute('SELECT COUNT(*) FROM ordenes').fetchone()[0]==1

def test_completar_informacion():
    assert procesar_solicitud('INC-035',usar_rag=False)['accion']=='solicitar_info'
    r=procesar_solicitud('INC-035','Pantalla negra al encender',usar_rag=False)
    assert r['accion']=='resolver_estandar' and r['orden']['ok']

def test_inexistente_sin_escritura():
    assert not procesar_solicitud('INC-999',usar_rag=False)['ok']
    with conectar() as c:
        assert c.execute('SELECT COUNT(*) FROM historial_solicitante').fetchone()[0]==0

def test_buffer_conversacion():
    memoria=crear_memoria_corto_plazo()
    procesar_solicitud('INC-001',memoria=memoria,usar_rag=False)
    assert len(memoria.chat_memory.messages)==2
    assert 'INC-001' in memoria.chat_memory.messages[0].content
    assert crear_memoria_corto_plazo().chat_memory.messages==[]

def test_rag_en_flujo(monkeypatch):
    from agent import core
    from langchain_core.tools import tool
    @tool
    def recuperar(texto: str) -> list[dict]:
        """Doble aislado para probar la integración de fuentes en el flujo."""
        return [{'tipo':'politica','texto':'Cobertura vigente','meta':{'fuente':'politicas.md'}}]
    monkeypatch.setattr(core,'buscar_casos_similares',recuperar)
    assert procesar_solicitud('INC-001')['fuentes'][0]['meta']['fuente']=='politicas.md'

def test_fallo_rag_visible(monkeypatch):
    from agent import core
    from langchain_core.tools import tool
    @tool
    def recuperar(texto: str) -> list[dict]:
        """Simula caída de la recuperación semántica."""
        raise RuntimeError('Sin índice')
    monkeypatch.setattr(core,'buscar_casos_similares',recuperar)
    r=procesar_solicitud('INC-001')
    assert r['ok'] and 'aviso' in r and r['fuentes']==[]
