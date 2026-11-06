from dataclasses import dataclass
from config.settings import UMBRAL_APROBACION, UMBRAL_PREFERENTE, UMBRAL_RECURRENCIA

@dataclass(frozen=True)
class Accion:
    tipo: str
    razon: str

def decidir_accion(estado: dict) -> Accion:
    """Aplica seis reglas ordenadas; la primera coincidencia determina el plan."""
    if not estado.get('elegible',False):
        return Accion('escalar',estado.get('razon','Sin cobertura validada'))
    if estado.get('costo',0)>UMBRAL_APROBACION:
        return Accion('solicitar_aprobacion',f'Costo ${estado["costo"]:,} supera ${UMBRAL_APROBACION:,}')
    if estado.get('incidentes_previos',0)>=UMBRAL_RECURRENCIA:
        return Accion('escalar_recurrencia',f'{estado["incidentes_previos"]} incidentes en 90 días; investigar causa raíz')
    if estado.get('solicitante_recurrente') and estado.get('costo',0)<UMBRAL_PREFERENTE and not estado.get('falta_info'):
        return Accion('resolver_preferente','Solicitante conocido, contexto completo y costo bajo')
    if estado.get('falta_info'):
        return Accion('solicitar_info','Falta descripción de la falla')
    return Accion('resolver_estandar','Incidente cubierto, completo y dentro de umbrales')

def construir_estado(ticket: dict, validacion: dict, descripcion: str = '') -> dict:
    return {'elegible':validacion.get('elegible',False),
            'razon':validacion.get('razon',''), 'costo':ticket['costo_estimado'],
            'incidentes_previos':ticket.get('incidentes_previos_90d',0),
            'solicitante_recurrente':bool(ticket.get('historial_solicitante')),
            'falta_info':not (descripcion.strip() or ticket.get('descripcion','').strip())}
