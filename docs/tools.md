# Contratos de las siete herramientas

| Herramienta | Entrada | Resultado y efecto |
|---|---|---|
| consultar_ticket | ticket_id | Incidente, historial y conteo en 90 días |
| validar_sla | ticket_id | Cobertura, cumplimiento y motivo |
| calcular_prioridad | ticket_id | P1, P2 o P3 y tiempo objetivo |
| generar_orden | ticket_id, descripcion opcional | Orden local única; valida reglas antes de escribir |
| actualizar_crm | ticket_id, estado, nota, descripcion | Un evento de decisión; rechaza estados incompatibles |
| notificar_solicitante | solicitante_id, mensaje | Notificación persistida, canal mock |
| buscar_casos_similares | texto | Dos políticas y dos casos con fuente y sección |
