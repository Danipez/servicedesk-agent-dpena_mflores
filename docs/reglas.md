# Reglas de decisión

| Prioridad | Condición | Acción |
|---|---|---|
| 1 | Cobertura vencida o SLA excedido | escalar |
| 2 | Costo > $100.000 CLP | solicitar_aprobacion |
| 3 | ≥ 3 incidentes en 90 días | escalar_recurrencia |
| 4 | Historial, costo < $50.000 y descripción completa | resolver_preferente |
| 5 | Sin descripción | solicitar_info |
| 6 | Resto de casos cubiertos | resolver_estandar |

El orden es estricto y la primera coincidencia determina la acción. La regla 4 exige información completa para evitar que la preferencia omita datos necesarios. Un escalamiento o una solicitud de aprobación no generan órdenes. P1 identifica impacto empresarial, P2 urgencia alta individual y P3 el resto. El escenario usa horas transcurridas simuladas, no un reloj de SLA productivo.
