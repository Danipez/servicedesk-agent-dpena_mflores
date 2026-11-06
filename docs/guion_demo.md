# Guion de exposición de nueve minutos y treinta segundos

La presentación tiene diez diapositivas. Las notas del expositor incluyen el argumento y la duración de cada una. El tiempo total planificado es 9:30, con 30 segundos de margen respecto del máximo de diez minutos.

| Tiempo | Diapositiva | Responsable | Contenido |
|---|---|---|---|
| 0:00 a 0:25 | 1 | Daniela Peña | Presentación del agente y del problema |
| 0:25 a 1:05 | 2 | Daniela Peña | Antecedentes necesarios antes de asignar soporte |
| 1:05 a 1:50 | 3 | Daniela Peña | Flujo de atención y siete herramientas |
| 1:50 a 2:45 | 4 | Daniela Peña | Seis reglas y orden de prioridad |
| 2:45 a 3:30 | 5 | Daniela Peña | Buffer, SQLite y recuperación semántica |
| 3:30 a 4:15 | 6 | Mirko Flores | Justificación de componentes y elección de LangChain |
| 4:15 a 6:45 | 7 | Mirko Flores | Demo con INC-001, INC-015 e INC-022 |
| 6:45 a 8:00 | 8 | Mirko Flores | Repetir INC-001 y mostrar el cambio por memoria |
| 8:00 a 8:55 | 9 | Ambos | Evidencia de pruebas y consultas Gemini |
| 8:55 a 9:30 | 10 | Ambos | Resultado y siguiente etapa |

## Preparación

Antes del ensayo, ejecutar `python -m scripts.seed_data` para comenzar con una base sin atenciones previas. Este comando recrea la base local y elimina su historial. Abrir la aplicación con `iniciar.cmd` o `python -m streamlit run app.py`. Tener el PowerPoint y la aplicación listos antes de empezar el cronómetro.

## Demostración del caso

1. En Procesar incidente, ingresar INC-001 y dejar vacía la descripción adicional. Mostrar resolver_estandar, prioridad P3 y código de orden.
2. Procesar INC-015. Mostrar que la falta de cobertura deriva el caso y evita generar una orden.
3. Procesar INC-022. Mostrar el costo de $250.000 CLP y solicitar_aprobacion.
4. Abrir la traza de un caso para explicar las herramientas ejecutadas.
5. En la siguiente diapositiva, repetir INC-001 sin reiniciar la base. Mostrar resolver_preferente y comprobar que conserva el mismo código de orden.

Nueva conversación limpia los mensajes y conserva el historial de SQLite. El personal técnico realiza la atención posterior. La aplicación registra la asignación, las decisiones y las notificaciones locales.

## Respaldo de la exposición

Si la aplicación no está disponible, usar las capturas incorporadas en las diapositivas y `evidence/demo_resultados.json`. Las decisiones estructuradas funcionan sin cuota de Gemini. La consulta conversacional puede mostrarse con «Consulta INC-035 y dime qué información falta» si queda tiempo dentro del máximo.
