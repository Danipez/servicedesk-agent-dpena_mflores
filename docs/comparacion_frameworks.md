# Comparación de frameworks

Se recomienda LangChain para este encargo por continuidad con el tutorial, que define @tool, AgentExecutor, ConversationBufferMemory e integración de Gemini y Chroma. La recomendación corresponde a este proyecto; no establece un ganador universal.

| Criterio | LangChain | Haystack |
|---|---|---|
| Fidelidad a la guía | Conserva las interfaces del ejemplo | Requiere adaptar agente, herramientas y estado |
| Agente con herramientas | AgentExecutor en la rama 0.3 utilizada | Componente Agent con ciclo de herramientas |
| Memoria y contexto | Buffer de conversación, SQLite y Chroma integrados en este proyecto | Estado y componentes de almacenamiento disponibles |
| Recuperación documental | Integración con Chroma y embeddings | Componentes y pipelines especialmente adecuados para organizar recuperación |
| Mantenimiento | Esta versión conserva APIs antiguas; migración futura explícita | Migrar exige reimplementar y validar el flujo de la guía |

La documentación oficial de LangChain describe llamadas a herramientas para Gemini. La de Haystack documenta Agent, herramientas y estado compartido. Ambos son viables. Para un nuevo sistema cuyo trabajo principal fuera construir pipelines documentales, Haystack merece una evaluación comparativa mediante datos y métricas propias. Aquí el objetivo es una automatización de soporte fiel al recorrido técnico solicitado.

Fuentes: https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai y https://docs.haystack.deepset.ai/docs/agents
