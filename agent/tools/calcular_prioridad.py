from langchain_core.tools import tool
from agent.storage import conectar

@tool
def calcular_prioridad(ticket_id: str) -> dict:
    """Calcula prioridad P1 a P3 desde impacto y urgencia del incidente."""
    with conectar() as conn:
        r=conn.execute('SELECT impacto,urgencia FROM tickets WHERE ticket_id=?',(ticket_id,)).fetchone()
    if r is None:
        return {'error':'Ticket no encontrado'}
    prioridad='P1' if r['impacto']=='empresa' else ('P2' if r['urgencia']=='alta' else 'P3')
    return {'prioridad':prioridad,'tiempo_objetivo_horas':{'P1':2,'P2':8,'P3':24}[prioridad]}
