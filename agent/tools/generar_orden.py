import uuid
from langchain_core.tools import tool
from agent.storage import conectar
from agent.tools.consultar_ticket import consultar_ticket
from agent.tools.validar_sla import validar_sla
from agent.tools.calcular_prioridad import calcular_prioridad
from agent.planner import construir_estado, decidir_accion

@tool
def generar_orden(ticket_id: str, descripcion: str = '') -> dict:
    """Genera una orden mock solo si el planner autoriza atención; reutiliza la existente."""
    ticket=consultar_ticket.invoke({'ticket_id':ticket_id})
    if 'error' in ticket:
        return ticket
    accion=decidir_accion(construir_estado(ticket,validar_sla.invoke({'ticket_id':ticket_id}),descripcion))
    if not accion.tipo.startswith('resolver_'):
        return {'ok':False,'error':'Orden bloqueada por política','accion':accion.tipo}
    prioridad=calcular_prioridad.invoke({'ticket_id':ticket_id})['prioridad']
    codigo=f'OT-{ticket_id}-{uuid.uuid4().hex[:6].upper()}'
    with conectar() as conn:
        conn.execute('INSERT OR IGNORE INTO ordenes VALUES (?,?,?,?,?)',
                     (ticket_id,codigo,prioridad,'Soporte nivel 1','pendiente'))
        r=conn.execute('SELECT * FROM ordenes WHERE ticket_id=?',(ticket_id,)).fetchone()
    return {'ok':True,**dict(r),'simulada':True}
