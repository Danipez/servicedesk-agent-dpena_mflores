"""Interfaz de atención y demostración de ServiceDesk Andina."""
import pandas as pd
import streamlit as st
from agent.core import procesar_solicitud, crear_agente
from agent.memory.short_term import crear_memoria_corto_plazo
from config.settings import DB_PATH

st.set_page_config(page_title='ServiceDesk Andina',page_icon='🛠️',layout='wide')
if 'memoria' not in st.session_state:
    st.session_state.memoria=crear_memoria_corto_plazo()
if 'historial' not in st.session_state:
    st.session_state.historial=[]
with st.sidebar:
    st.title('🛠️ ServiceDesk Andina')
    st.caption('Agente de soporte empresarial · EP2 ISY0101')
    st.markdown('### Casos de ejemplo')
    st.code('INC-001 → estándar\nINC-015 → sin cobertura\nINC-022 → alto costo\nINC-030 → recurrencia\nINC-035 → falta información\nINC-040 → SLA excedido')
    st.caption('Repetir INC-001 demuestra atención preferente por memoria.')
    if st.button('🔄 Nueva conversación'):
        st.session_state.historial=[]
        st.session_state.memoria=crear_memoria_corto_plazo()
        st.session_state.pop('agente',None)
        st.rerun()
    st.caption('La nueva conversación borra el buffer, conserva el historial persistente.')
st.title('Agente de Soporte ServiceDesk Andina')
st.write('Automatización de la recepción y asignación de incidentes de soporte. '
         'El agente valida cobertura y SLA, genera órdenes o deriva a revisión humana.')
st.caption('Entorno simulado: no se envían correos ni se realizan reparaciones o compras reales.')
if not DB_PATH.exists():
    st.error('Prepara los datos: python -m scripts.generate_mock_data y python -m scripts.seed_data')
    st.stop()
atencion, conversacion=st.tabs(['Procesar incidente','Asistente Gemini'])
with atencion:
    col1,col2=st.columns([1,2])
    with col1:
        ticket_id=st.text_input('ID de incidente',value='INC-001')
        descripcion=st.text_input('Descripción adicional (opcional)',value='')
        ejecutar=st.button('▶️ Procesar incidente',type='primary')
    if ejecutar:
        with st.spinner('Consultando contexto y evaluando políticas...'):
            try:
                resultado=procesar_solicitud(ticket_id,descripcion,st.session_state.memoria)
            except Exception:
                resultado={'ok':False,'ticket_id':ticket_id,'error':'No se pudo procesar el incidente. Comprueba la base de datos y sus permisos.'}
        st.session_state.historial.append(resultado)
    if st.session_state.historial:
        ultimo=st.session_state.historial[-1]
        if not ultimo.get('ok'):
            st.error(ultimo.get('error','No se completó el flujo'))
        else:
            st.subheader(f'Resultado para {ultimo["ticket_id"]}')
            colores={'resolver_estandar':'green','resolver_preferente':'green',
                'solicitar_aprobacion':'orange','escalar':'red','escalar_recurrencia':'red','solicitar_info':'blue'}
            st.markdown(f'### :{colores[ultimo["accion"]]}[Acción: `{ultimo["accion"]}`]')
            st.caption(f'**Razón:** {ultimo["razon"]}')
            st.write(f'Prioridad: **{ultimo["prioridad"]["prioridad"]}** · Costo estimado: **${ultimo["ticket"]["costo_estimado"]:,} CLP**')
            if ultimo.get('orden'):
                st.success(f'Orden de atención simulada: {ultimo["orden"]["codigo"]}')
            if ultimo.get('aviso'):
                st.warning(ultimo['aviso'])
            with st.expander('🔍 Decisión y traza de herramientas',expanded=True):
                st.json({'validacion':ultimo['validacion'],'accion':ultimo['accion'],'razon':ultimo['razon']})
                st.json(ultimo['trace'],expanded=False)
            with st.expander('🧠 Memoria recuperada del solicitante'):
                st.dataframe(pd.DataFrame(ultimo['ticket']['historial_solicitante']),width='stretch')
                st.write('Incidentes en 90 días:',ultimo['ticket']['incidentes_previos_90d'])
            with st.expander('📚 Políticas y casos recuperados'):
                for fuente in ultimo['fuentes']:
                    st.write(fuente['texto'])
                    st.caption(str(fuente['meta']))
    if st.session_state.historial:
        st.divider()
        st.subheader('📜 Historial de la sesión')
        st.dataframe(pd.DataFrame([{'incidente':r['ticket_id'],'acción':r.get('accion','error'),
            'razón':r.get('razon',r.get('error',''))} for r in st.session_state.historial]),width='stretch')
with conversacion:
    st.write('Consulta políticas o solicita atención en lenguaje natural. El asistente puede utilizar las siete herramientas.')
    pregunta=st.text_input('Pregunta al agente',placeholder='Consulta INC-022 y explica por qué requiere aprobación')
    if st.button('Consultar con Gemini') and pregunta.strip():
        with st.spinner('Consultando al asistente...'):
            try:
                if 'agente' not in st.session_state:
                    st.session_state.agente=crear_agente(st.session_state.memoria)
                respuesta=st.session_state.agente.invoke({'input':pregunta})
                st.write(respuesta['output'])
                with st.expander('Herramientas ejecutadas'):
                    st.json([{'herramienta':a.tool,'entrada':a.tool_input,'salida':v} for a,v in respuesta['intermediate_steps']])
            except Exception:
                st.error('Gemini no pudo responder. Revisa la clave, el modelo, la cuota y la conexión. La atención estructurada sigue disponible.')
    with st.expander('Memoria de la conversación'):
        for mensaje in st.session_state.memoria.chat_memory.messages:
            st.write(f'{mensaje.type}: {mensaje.content}')
