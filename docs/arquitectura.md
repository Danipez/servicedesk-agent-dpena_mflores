# Arquitectura y memorias

La interfaz mantiene la distribución de la guía: barra lateral con casos, formulario de incidente y descripción, decisión con color, traza, memoria e historial. Agrega una pestaña para usar el AgentExecutor real con Gemini y las siete herramientas.

## Dos rutas de ejecución

`procesar_solicitud` usa herramientas LangChain y un planner determinista. Recupera contexto semántico y ejecuta solo las acciones permitidas. `crear_agente` construye un AgentExecutor de LangChain con llamadas a herramientas, temperatura 0,2 y límite de ocho iteraciones. Las dos rutas comparten herramientas y controles de escritura. La ruta estructurada no requiere Gemini; sí necesita el modelo de embeddings ya descargado para RAG.

## Memoria de corto plazo

ConversationBufferMemory conserva mensajes en RAM y st.session_state. El flujo estructurado guarda solicitud y resultado; el agente Gemini incorpora chat_history en su prompt. Nueva conversación crea un buffer vacío y conserva SQLite. Esta API corresponde a LangChain 0.3, fijado deliberadamente por compatibilidad con el tutorial.

## Memoria de largo plazo

SQLite guarda decisiones, órdenes y notificaciones. consultar_ticket recupera tres decisiones recientes y cuenta antecedentes más tickets distintos atendidos en 90 días. El caso INC-001 cambia de resolver_estandar a resolver_preferente tras la primera atención. La orden es única por incidente, por lo que repetir la demostración no duplica órdenes. El historial conserva un evento por solicitud; no equivale al número de incidentes distintos.

## Memoria semántica

all-MiniLM-L6-v2 genera embeddings locales. Chroma persiste dos colecciones: seis secciones de políticas y cuatro casos de referencia. buscar_casos_similares recupera dos resultados de cada colección con metadatos. La indexación utiliza identificadores estables. No se suben los vectores: se reconstruyen con el script. Una falla de recuperación deja un aviso visible y mantiene las reglas estructuradas.

## Compatibilidad de Gemini

El agente conserva AgentExecutor y las herramientas del stack LangChain 0.3 de la guía. El adaptador `agent/gemini.py` implementa BaseChatModel con la API REST oficial y conserva completos los `parts` de respuestas Gemini, incluidas las firmas de llamadas a herramientas. Esto permite usar Gemini 3.5 Flash con el ciclo de herramientas antiguo; el conector Google anterior pierde esa información. La prueba simple verify_llm conserva el conector del tutorial; verify_agent verifica la ruta completa utilizada por la aplicación. Referencia: https://ai.google.dev/gemini-api/docs/thought-signatures

## Integridad y límites

Las consultas usan parámetros SQL. generar_orden verifica nuevamente el planner y reutiliza la orden existente. actualizar_crm rechaza estados incompatibles. El registro y la notificación son operaciones separadas: ante una caída entre ambas puede quedar una decisión sin notificación; una solución productiva requeriría transacción de caso y patrón outbox. Los escenarios concurrentes y las autorizaciones posteriores no están implementados.
