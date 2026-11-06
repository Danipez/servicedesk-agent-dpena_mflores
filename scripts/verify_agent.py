"""Verifica dos turnos reales de Gemini con consulta, herramientas y memoria."""
import json
from agent.core import crear_agente
from agent.memory.short_term import crear_memoria_corto_plazo
from config.settings import BASE_DIR, LLM_MODEL

def verificar():
    memoria=crear_memoria_corto_plazo()
    agente=crear_agente(memoria)
    consultas=['Consulta INC-022 con consultar_ticket y validar_sla. '
               'Busca su política con buscar_casos_similares y explica por qué requiere aprobación. No escribas cambios.',
               '¿Cuál era el número y costo del incidente que acabamos de revisar?']
    registros=[]
    for consulta in consultas:
        r=agente.invoke({'input':consulta})
        pasos=[{'herramienta':a.tool,'entrada':a.tool_input,'salida':v} for a,v in r['intermediate_steps']]
        registros.append({'consulta':consulta,'respuesta':r['output'],'herramientas':pasos})
        print('Turno completado:',len(pasos),'herramientas')
    nombres={p['herramienta'] for p in registros[0]['herramientas']}
    assert {'consultar_ticket','validar_sla','buscar_casos_similares'}<=nombres
    assert 'INC-022' in registros[1]['respuesta']
    assert len(memoria.chat_memory.messages)==4
    (BASE_DIR/'evidence/gemini_agent.json').write_text(json.dumps(
        {'modelo':LLM_MODEL,'mensajes_memoria':len(memoria.chat_memory.messages),'turnos':registros},
        ensure_ascii=False,indent=2),encoding='utf-8')
    print('Agente y memoria conversacional verificados.')

if __name__=='__main__':
    verificar()
