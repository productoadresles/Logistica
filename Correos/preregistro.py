from pydantic import BaseModel
from typing import Optional
from typing import List


## Pre registro response package list
class PreRegister_Response_File(BaseModel):
    nombreFicheiro: str
    tipoDoc: str
    ficheiroBinario: str
    
## Pre registro response package list
class PreRegister_Response_Package(BaseModel):
    numBulto: int
    codEnvio: str
    codManifiesto: str
    ficheiro: PreRegister_Response_File

## Pre registro response
class PreRegister_Response(BaseModel):
    resultado: int
    codExpedicion: str
    fechaRespuesta: str
    bultos: List[PreRegister_Response_Package]

## Pre registro package request     
class Package(BaseModel):
    peso: int
    observaciones_salida: Optional[str] = None

## Pre registro shipment request
class Shipment(BaseModel):
    prod: int
    id_agencia: str
    cantidad: int
    client_uid: str
    codigos_origen: str
    codigos_destino: str
    direccion_salida: str
    direccion_llegada: str
    email_llegada: str
    email_salida: str
    poblacion_llegada: str
    poblacion_salida: str
    telefono_llegada: Optional[str] = None
    telefono_salida: str
    fecha_operacion: str
    nombre_llegada: str
    nombre_salida: str
    packageList: List[Package]
