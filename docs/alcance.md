# Alcance de ServiceDesk Andina

ServiceDesk Andina representa una empresa ficticia de servicios administrativos que recibe incidentes de equipos y aplicaciones por distintos canales. La clasificación manual demora la asignación, repite consultas y dificulta reconocer fallas recurrentes. El agente automatiza el triage y la creación de órdenes de atención con políticas trazables.

Recibe un ID o una solicitud en lenguaje natural, recupera contexto, valida cobertura y SLA, calcula prioridad, genera una orden mock o deriva el caso. Conserva historial entre sesiones y cita políticas recuperadas. Las notificaciones se guardan localmente. El beneficio que se busca es reducir pasos manuales; no se presenta como una mejora medida en una empresa real.

No repara equipos, compra repuestos, realiza pagos ni envía correos. Las aprobaciones de jefatura y la resolución técnica quedan fuera del alcance. La cobertura, el impacto y la urgencia se consideran datos confiables del conjunto simulado. Un despliegue empresarial necesitaría autenticación, autorización por rol y un reloj SLA real.

La demostración debe recorrer atención estándar, falta de cobertura, aprobación por costo y cambio por memoria en diez minutos. La latencia de cada ejecución se registra en evidence/demo_resultados.json; no se garantiza un tiempo para todos los equipos ni para Gemini.
