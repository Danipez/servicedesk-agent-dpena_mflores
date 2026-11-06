# Guion de demostración de diez minutos

| Tiempo | Responsable | Acción y evidencia |
|---|---|---|
| 0:00 a 1:00 | Daniela Peña | Explicar el problema de asignación manual y el alcance simulado |
| 1:00 a 2:30 | Daniela Peña | Abrir Streamlit, procesar INC-001, mostrar orden y traza |
| 2:30 a 4:00 | Daniela Peña | Repetir INC-001, mostrar atención preferente y memoria recuperada |
| 4:00 a 5:30 | Mirko Flores | Procesar INC-015 y demostrar ausencia de orden por cobertura |
| 5:30 a 6:30 | Mirko Flores | Procesar INC-022, mostrar aprobación requerida y costo |
| 6:30 a 7:30 | Mirko Flores | Procesar INC-030 y explicar escalamiento por recurrencia |
| 7:30 a 8:30 | Ambos | Mostrar políticas recuperadas y diagrama de orquestación |
| 8:30 a 9:30 | Ambos | Preguntar a Gemini por INC-022 y mostrar herramientas, si la cuota lo permite |
| 9:30 a 10:00 | Ambos | Mostrar resultados de pruebas y exponer su evaluación personal |

Preparación: ejecutar scripts.seed_data antes del ensayo; no reiniciar entre los dos pasos de INC-001. Nueva conversación limpia mensajes, no la memoria persistente. Para demostrar datos incompletos, procesar INC-035 sin descripción y repetir con “Pantalla negra al encender”.

Preguntas de preparación: ¿por qué la primera regla tiene prioridad?, ¿qué diferencia hay entre evento e incidente distinto?, ¿cómo se reconstruye Chroma?, ¿qué sucede sin Gemini?, ¿qué falta para producción? Cada integrante debe preparar y defender sus respuestas con el código y las evidencias.

Plan de respaldo: dejar los embeddings descargados, conservar capturas y evidence/demo_resultados.json. La atención estructurada no depende de cuota Gemini. El video de los expositores y los ensayos deben realizarlos los integrantes.
