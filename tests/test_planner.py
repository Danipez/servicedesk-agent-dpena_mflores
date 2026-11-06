import pytest
from agent.planner import decidir_accion

@pytest.mark.parametrize('cambios,esperado',[
    ({'elegible':False},'escalar'),
    ({'costo':100001},'solicitar_aprobacion'),
    ({'incidentes_previos':3},'escalar_recurrencia'),
    ({'solicitante_recurrente':True,'costo':49999},'resolver_preferente'),
    ({'falta_info':True},'solicitar_info'),
    ({},'resolver_estandar'),
    ({'costo':100000},'resolver_estandar'),
    ({'solicitante_recurrente':True,'costo':50000},'resolver_estandar'),
    ({'elegible':False,'costo':250000,'incidentes_previos':5},'escalar'),
    ({'costo':250000,'incidentes_previos':5},'solicitar_aprobacion'),
    ({'solicitante_recurrente':True,'falta_info':True},'solicitar_info'),
])
def test_reglas_y_fronteras(cambios,esperado):
    estado={'elegible':True,'costo':25000,'incidentes_previos':0,'falta_info':False}
    estado.update(cambios)
    assert decidir_accion(estado).tipo==esperado
