from langchain_core.tools import tool
from agent.storage import conectar

@tool
def validar_sla(ticket_id: str) -> dict:
    """Valida cobertura, tiempo SLA y necesidad de atención especializada."""
    with conectar() as conn:
        r=conn.execute('SELECT * FROM tickets WHERE ticket_id=?',(ticket_id,)).fetchone()
    if r is None:
        return {'elegible':False,'razon':'Ticket no encontrado'}
    limite=2 if r['impacto']=='empresa' else 24
    if r['cobertura']!='vigente':
        return {'elegible':False,'razon':'Cobertura de soporte vencida', 'sla_horas':limite}
    if r['horas_transcurridas']>limite:
        return {'elegible':False,'razon':f'SLA excedido: {r["horas_transcurridas"]} horas, máximo {limite}', 'sla_horas':limite}
    return {'elegible':True,'razon':'Cobertura vigente y dentro de SLA', 'sla_horas':limite}
