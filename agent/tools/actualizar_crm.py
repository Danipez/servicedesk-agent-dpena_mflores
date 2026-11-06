from langchain_core.tools import tool
from agent.memory.long_term import guardar_decision
from agent.tools.consultar_ticket import consultar_ticket
from agent.tools.validar_sla import validar_sla
from agent.planner import construir_estado, decidir_accion

@tool
def actualizar_crm(ticket_id: str, estado: str, nota: str = '', descripcion: str = '') -> dict:
    """Guarda el estado de atención si coincide con la decisión vigente del planner."""
    ticket=consultar_ticket.invoke({'ticket_id':ticket_id})
    if 'error' in ticket:
        return {'ok':False,**ticket}
    accion=decidir_accion(construir_estado(ticket,validar_sla.invoke({'ticket_id':ticket_id}),descripcion))
    if estado!=accion.tipo:
        return {'ok':False,'error':'Estado rechazado por política','accion_esperada':accion.tipo}
    guardar_decision(ticket['solicitante_id'],ticket_id,estado,ticket['costo_estimado'],nota or accion.razon)
    return {'ok':True,'estado':estado}
