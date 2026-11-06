"""Genera 40 incidentes y 15 solicitantes ficticios con semilla reproducible."""
import csv
import random
from datetime import timedelta
from config.settings import DATA_DIR, DEMO_DATE

def generar():
    rng = random.Random(42)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    catalogo = [('Mouse no responde', 'periferico', 25000),
                ('Impresora sin conexión', 'impresora', 65000),
                ('Equipo no inicia', 'equipo', 85000),
                ('Aplicación se cierra', 'software', 15000)]
    with (DATA_DIR / 'tickets.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['ticket_id','solicitante_id','asunto','categoria','costo_estimado',
                    'fecha_apertura','cobertura','descripcion','impacto','urgencia','horas_transcurridas'])
        for i in range(1,41):
            asunto, categoria, costo = rng.choice(catalogo)
            descripcion = 'Falla persistente tras reiniciar. Se requiere atención técnica.'
            cobertura, impacto, urgencia, horas = 'vigente', 'individual', 'normal', rng.randint(1,8)
            solicitante = f'S-{rng.randint(1,15):03d}'
            if i == 1:
                asunto, categoria, costo, solicitante = 'Mouse no responde', 'periferico', 25000, 'S-001'
            elif i == 15:
                cobertura, horas, solicitante = 'vencida', 45, 'S-015'
            elif i == 22:
                asunto, categoria, costo, solicitante = 'Servidor requiere repuesto', 'servidor', 250000, 'S-022'
                solicitante = 'S-012'
            elif i == 30:
                solicitante, costo = 'S-003', 40000
            elif i == 35:
                solicitante, descripcion = 'S-005', ''
            elif i == 40:
                impacto, urgencia, horas = 'empresa', 'alta', 3
            fecha = (DEMO_DATE - timedelta(days=rng.randint(0,2))).isoformat()
            w.writerow([f'INC-{i:03d}',solicitante,asunto,categoria,costo,fecha,
                        cobertura,descripcion,impacto,urgencia,horas])
    with (DATA_DIR / 'solicitantes.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f)
        w.writerow(['solicitante_id','nombre','email','incidentes_previos_90d'])
        for i in range(1,16):
            w.writerow([f'S-{i:03d}',f'Solicitante {i}',f'solicitante{i}@example.com',3 if i==3 else 0])
    print('Generados 40 incidentes y 15 solicitantes.')

if __name__ == '__main__':
    generar()
