from datetime import datetime, timezone
from langchain_core.tools import tool
from agent.storage import conectar

@tool
def notificar_solicitante(solicitante_id: str, mensaje: str) -> dict:
    """Registra una notificación local simulada; no envía correo ni SMS reales."""
    if not mensaje.strip():
        return {'ok':False,'error':'El mensaje está vacío'}
    with conectar() as conn:
        if not conn.execute('SELECT 1 FROM solicitantes WHERE solicitante_id=?',(solicitante_id,)).fetchone():
            return {'ok':False,'error':'Solicitante no encontrado'}
        conn.execute('INSERT INTO notificaciones(solicitante_id,fecha,mensaje,canal) VALUES (?,?,?,?)',
                     (solicitante_id,datetime.now(timezone.utc).isoformat(),mensaje,'mock'))
    return {'ok':True,'canal':'mock','solicitante_id':solicitante_id}
