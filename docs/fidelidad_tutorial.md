# Correspondencia con el tutorial

El caso de devoluciones se reemplaza por recepción y asignación de incidentes de soporte empresarial. Se conserva la arquitectura del tutorial sin reutilizar sus pedidos ni sus políticas de devolución.

| Fase | Evidencia en este proyecto |
|---|---|
| 0 Entorno | requirements, .env.example, verify_llm |
| 1 Alcance y contratos | docs/alcance.md, tools.md y reglas.md |
| 2 Datos | 40 tickets, 15 solicitantes y carga SQLite |
| 3 Herramientas | Siete funciones con @tool y docstrings en español |
| 4 Memoria | Buffer de conversación y eventos SQLite |
| 5 Semántica | Chroma, MiniLM, seis secciones y cuatro casos |
| 6 Planner | Seis reglas priorizadas y pruebas de frontera |
| 7 Integración | Flujo determinista y AgentExecutor con Gemini |
| 8 Interfaz | Streamlit con formulario, colores, traza e historial |
| 9 Pruebas | Suite aislada y evidencia guardada |
| 10 Documentación | README, Mermaid, informe y referencias |
| 11 Demo | Guion de diez minutos y escenarios reproducibles |

Ajustes funcionales: historial escrito una sola vez por ejecución; órdenes únicas por ticket; fixture con base temporal por prueba; regla preferente exige descripción; datos especiales garantizados; índices con IDs estables; buffer conectado realmente al prompt. El modelo se configura por variable y se verifica con la cuenta utilizada.

El correo indica 10 minutos de exposición y 5 de preguntas; la pauta y la guía indican 10 y 10. El guion usa 10 minutos de exposición, compatible con ambas instrucciones. Las ponderaciones del correo y la pauta también difieren; corresponde al docente definir cuál aplica.
