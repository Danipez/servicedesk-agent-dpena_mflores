# Política de atención ServiceDesk Andina

## Cobertura y SLA
Solo los activos con cobertura vigente pueden generar órdenes automáticas. El SLA es de 24 horas para incidentes individuales y 2 horas para impacto en toda la empresa. Un incumplimiento exige escalamiento humano.

## Costos
Un costo estimado mayor a $100.000 CLP requiere autorización de la jefatura. El agente no compra repuestos ni realiza pagos. El límite es estricto: $100.000 no activa aprobación adicional.

## Recurrencia
Tres o más incidentes del mismo solicitante en 90 días requieren revisión de causa raíz por soporte nivel 2. El conteo incluye antecedentes registrados y tickets distintos atendidos, sin duplicar reintentos del mismo ticket.

## Atención preferente
Si existe historial de atención, el costo es menor a $50.000 y la descripción está completa, se genera orden preferente. Un historial previo no autoriza saltarse cobertura, costo ni recurrencia.

## Información requerida
El número de incidente y una descripción de la falla son necesarios. Si falta descripción, se solicita información antes de generar una orden. Un texto nuevo puede completar el incidente pendiente.

## Atención estándar y comunicación
Un incidente cubierto y completo que no activa una regla anterior sigue el flujo estándar. La prioridad P1 corresponde a impacto empresarial, P2 a urgencia alta individual y P3 al resto. Las órdenes y notificaciones se registran en SQLite para auditoría. Las notificaciones utilizan el canal local.
