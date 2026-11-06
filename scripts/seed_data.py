"""Recrea la base de demostración; elimina su historial previo."""
import csv
import sqlite3
from contextlib import closing
from config import settings

def cargar(db_path=None):
    path = db_path or settings.DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(path)) as conn, conn:
        conn.executescript("""
        DROP TABLE IF EXISTS tickets;
        DROP TABLE IF EXISTS solicitantes;
        DROP TABLE IF EXISTS historial_solicitante;
        DROP TABLE IF EXISTS ordenes;
        DROP TABLE IF EXISTS notificaciones;
        CREATE TABLE tickets(ticket_id TEXT PRIMARY KEY, solicitante_id TEXT, asunto TEXT,
            categoria TEXT, costo_estimado INTEGER, fecha_apertura TEXT, cobertura TEXT,
            descripcion TEXT, impacto TEXT, urgencia TEXT, horas_transcurridas INTEGER);
        CREATE TABLE solicitantes(solicitante_id TEXT PRIMARY KEY, nombre TEXT, email TEXT,
            incidentes_previos_90d INTEGER);
        CREATE TABLE historial_solicitante(id INTEGER PRIMARY KEY AUTOINCREMENT,
            solicitante_id TEXT, ticket_id TEXT, fecha TEXT, decision TEXT,
            costo INTEGER, motivo TEXT);
        CREATE TABLE ordenes(ticket_id TEXT PRIMARY KEY, codigo TEXT UNIQUE, prioridad TEXT,
            equipo TEXT, estado TEXT);
        CREATE TABLE notificaciones(id INTEGER PRIMARY KEY AUTOINCREMENT,
            solicitante_id TEXT, fecha TEXT, mensaje TEXT, canal TEXT);
        """)
        for filename, table in [('tickets.csv','tickets'),('solicitantes.csv','solicitantes')]:
            with (settings.DATA_DIR / filename).open(encoding='utf-8') as f:
                reader=csv.DictReader(f)
                columns=reader.fieldnames
                marks=','.join('?' for _ in columns)
                conn.executemany(f"INSERT INTO {table} ({','.join(columns)}) VALUES ({marks})",
                                 [tuple(row[c] for c in columns) for row in reader])
    print('SQLite de demostración preparado.')

if __name__ == '__main__':
    cargar()
