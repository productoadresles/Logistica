from pydantic import BaseModel
from typing import Optional
from typing import List


class Tracking_Response_Evento(BaseModel):
    fecEvento: str
    horEvento: str
    codEvento: str
    desTextoResumen: str
    desTextoAmpliado: str
    Emisiones: str

class Tracking_Response_EnvioAsociado(BaseModel):
    codEnvio: str
    fecEvento: str
    horEvento: str
    codEvento: str
    desResumen: str
    desAmpliada: str

class Tracking_Response_Error(BaseModel):
    codError: str
    desError: str

class Tracking_Response(BaseModel):
    codEnvio: str
    numReferencia1: str
    numReferencia2: str
    numReferencia3: str
    nombre_cliente: str
    eur_reembolso: str
    eventos: List[Tracking_Response_Evento]
    enviosAsociados: List[Tracking_Response_EnvioAsociado]
    Error: List[Tracking_Response_Error]
    largo: str
    alto: str
    ancho: str
    peso: str
    fec_entregasum: str
    codExpedicion: str
    totalBultos: str
    numBultos: str
    numRefExpedicion: str

#PQ43B404AA015110128001N