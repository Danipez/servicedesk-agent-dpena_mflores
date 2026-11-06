"""Genera evidencia reproducible en una base temporal sin alterar la demo local."""
import json
import tempfile
import time
from pathlib import Path
from config import settings
from scripts.seed_data import cargar
from agent.core import procesar_solicitud

def ejecutar():
    destino=settings.BASE_DIR/'evidence/demo_resultados.json'
    original=settings.DB_PATH
    with tempfile.TemporaryDirectory() as carpeta:
        settings.DB_PATH=Path(carpeta)/'demo.db'
        try:
            cargar()
            resultados=[]
            for ticket in ['INC-001','INC-001','INC-015','INC-022','INC-030','INC-035','INC-040']:
                inicio=time.perf_counter()
                r=procesar_solicitud(ticket)
                resultados.append({**r,'duracion_segundos':round(time.perf_counter()-inicio,3)})
                print(ticket,r.get('accion'),len(r.get('fuentes',[])),'fuentes')
            r=procesar_solicitud('INC-035','Pantalla negra al encender')
            resultados.append(r)
            destino.write_text(json.dumps(resultados,ensure_ascii=False,indent=2),encoding='utf-8')
            assert all(r['ok'] and len(r['fuentes'])==4 for r in resultados)
            assert resultados[0]['accion']=='resolver_estandar'
            assert resultados[1]['accion']=='resolver_preferente'
            assert resultados[-1]['accion']=='resolver_estandar'
        finally:
            settings.DB_PATH=original

if __name__=='__main__':
    ejecutar()
