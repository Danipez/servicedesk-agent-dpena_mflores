from datetime import datetime, timezone, timedelta
from agent.storage import conectar

def guardar_decision(solicitante_id, ticket_id, decision, costo, motivo):
    """Persiste una decisión de negocio como evento, una sola vez por flujo."""
    with conectar() as conn:
        conn.execute('INSERT INTO historial_solicitante '
            '(solicitante_id,ticket_id,fecha,decision,costo,motivo) VALUES (?,?,?,?,?,?)',
            (solicitante_id,ticket_id,datetime.now(timezone.utc).isoformat(),decision,costo,motivo))
    return {'ok':True}

def obtener_historial(solicitante_id, limite=5):
    """Recupera decisiones de otras sesiones, ordenadas por evento reciente."""
    with conectar() as conn:
        rows=conn.execute('SELECT * FROM historial_solicitante WHERE solicitante_id=? '
                          'ORDER BY id DESC LIMIT ?', (solicitante_id,limite)).fetchall()
    return [dict(r) for r in rows]

def contar_incidentes_recientes(solicitante_id):
    """Suma antecedentes mock y tickets distintos atendidos en los últimos 90 días."""
    limite=(datetime.now(timezone.utc)-timedelta(days=90)).isoformat()
    with conectar() as conn:
        base=conn.execute('SELECT incidentes_previos_90d FROM solicitantes '
                          'WHERE solicitante_id=?',(solicitante_id,)).fetchone()
        nuevos=conn.execute("SELECT COUNT(DISTINCT ticket_id) FROM historial_solicitante "
            "WHERE solicitante_id=? AND fecha>=? AND decision IN ('resolver_estandar','resolver_preferente')",
            (solicitante_id,limite)).fetchone()[0]
    return (int(base[0]) if base else 0)+nuevos
