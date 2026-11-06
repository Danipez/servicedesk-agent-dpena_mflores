from langchain_core.tools import tool
from agent.storage import conectar
from agent.memory.long_term import obtener_historial, contar_incidentes_recientes

@tool
def consultar_ticket(ticket_id: str) -> dict:
    """Consulta un incidente y recupera el historial de su solicitante."""
    with conectar() as conn:
        row=conn.execute('SELECT * FROM tickets WHERE ticket_id=?',(ticket_id,)).fetchone()
    if row is None:
        return {'error': f'Ticket {ticket_id} no encontrado'}
    ticket=dict(row)
    ticket['historial_solicitante']=obtener_historial(ticket['solicitante_id'],3)
    ticket['incidentes_previos_90d']=contar_incidentes_recientes(ticket['solicitante_id'])
    return ticket
