from agent.tools.consultar_ticket import consultar_ticket
from agent.tools.validar_sla import validar_sla
from agent.tools.calcular_prioridad import calcular_prioridad
from agent.tools.generar_orden import generar_orden
from agent.tools.actualizar_crm import actualizar_crm
from agent.tools.notificar_solicitante import notificar_solicitante
from agent.memory.long_term import obtener_historial
from agent.storage import conectar

def test_consulta_existente():
    r=consultar_ticket.invoke({'ticket_id':'INC-001'})
    assert r['costo_estimado']==25000 and r['historial_solicitante']==[]

def test_consulta_inexistente():
    assert 'error' in consultar_ticket.invoke({'ticket_id':'INC-999'})

def test_consulta_parametrizada():
    assert 'error' in consultar_ticket.invoke({'ticket_id':"INC-001' OR 1=1 --"})

def test_cobertura():
    assert validar_sla.invoke({'ticket_id':'INC-015'})['elegible'] is False

def test_sla():
    assert 'SLA' in validar_sla.invoke({'ticket_id':'INC-040'})['razon']

def test_validacion_inexistente():
    assert validar_sla.invoke({'ticket_id':'INC-999'})['elegible'] is False

def test_prioridad_critica():
    assert calcular_prioridad.invoke({'ticket_id':'INC-040'})['prioridad']=='P1'

def test_orden_idempotente():
    a=generar_orden.invoke({'ticket_id':'INC-001'})
    b=generar_orden.invoke({'ticket_id':'INC-001'})
    assert a['codigo']==b['codigo'] and a['almacenamiento']=='sqlite'

def test_orden_alto_costo_bloqueada():
    assert generar_orden.invoke({'ticket_id':'INC-022'})['ok'] is False

def test_crm_no_permite_saltar_reglas():
    r=actualizar_crm.invoke({'ticket_id':'INC-022','estado':'resolver_estandar'})
    assert r['ok'] is False
    assert obtener_historial('S-012')==[]

def test_crm_guarda_una_decision():
    assert actualizar_crm.invoke({'ticket_id':'INC-001','estado':'resolver_estandar'})['ok']
    assert len(obtener_historial('S-001'))==1

def test_notificacion_persistida():
    assert notificar_solicitante.invoke({'solicitante_id':'S-001','mensaje':'Orden lista'})['ok']
    with conectar() as c:
        assert c.execute('SELECT mensaje FROM notificaciones').fetchone()[0]=='Orden lista'

def test_notificacion_inexistente():
    assert notificar_solicitante.invoke({'solicitante_id':'S-999','mensaje':'Hola'})['ok'] is False
