from typing import Optional
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum
import random

import requests
from requests.auth import HTTPBasicAuth

import json
import xml.dom.minidom
import xmltodict

from vars import PICKUP_AUTH, PICKUP_PRE_AUTH, PICKUP_PRE_URL, PICKUP_URL, PR_PRE_URL, PR_URL, PREREGISTER_AUTH, PREREGISTER_PRE_AUTH

import xml.etree.ElementTree as ET
from datetime import datetime

null = 'null'
false = False

class back(BaseModel):
    servicio: str
    id_usuario: str



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
    
class Package(BaseModel):
    peso: int
    largo: Optional[int] = None
    alto: Optional[int] = None
    ancho: Optional[int] = None
    observaciones_salida: Optional[str] = None

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

class ReqStatus(BaseModel):
    prod: int
    id_agencia: str
    client_uid: str
    codigo_recogida: str

app = FastAPI()

handler = Mangum(app)

@app.get("/")
async def root():
    return {"message": "Hello World"}
    

@app.post("/PreRegister")
async def preregister_correos(req: Shipment):

    #auth = (user, password)
    auth = (PREREGISTER_PRE_AUTH if req.prod == 0 else PREREGISTER_AUTH)

    # URL CORREOS
    url = (PR_PRE_URL if req.prod == 0 else PR_URL)
    #print('URL: ',url)
    
    #  Generación de la referencia tipo C
    def random_with_N_digits(n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return random.randint(range_start, range_end)

    payload = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:prer="http://www.correos.es/iris6/services/preregistroetiquetas">
        <soapenv:Header/>
        <soapenv:Body>"""

    payload2 = f""""""
    
    #setup the first part of the shipment info (addresses and contacts)
    payloadB = f"""
        <prer:PreregistroEnvioMultibulto>
            <prer:FechaOperacion>{req.fecha_operacion}</prer:FechaOperacion>
            <prer:CodEtiquetador>XXX1</prer:CodEtiquetador>
            <prer:Care>000000</prer:Care>
            <prer:TotalBultos>{req.cantidad}</prer:TotalBultos>
            <prer:ModDevEtiqueta>2</prer:ModDevEtiqueta>
            <prer:Remitente>
            
                <prer:Identificacion>
                <prer:Nombre>{req.nombre_salida}</prer:Nombre>
                </prer:Identificacion>
                
                <prer:DatosDireccion>
                <prer:Direccion>{req.direccion_salida}</prer:Direccion>
                <prer:Localidad>{req.poblacion_salida}</prer:Localidad>
                </prer:DatosDireccion>
                
                <prer:CP>{req.codigos_origen}</prer:CP>
                <prer:Telefonocontacto>{req.telefono_salida}</prer:Telefonocontacto>
                <prer:Email>{req.email_salida}</prer:Email>
            
                <prer:DatosSMS>
                <prer:NumeroSMS>{req.telefono_salida}</prer:NumeroSMS>
                </prer:DatosSMS>
                
            </prer:Remitente>
            
            <prer:Destinatario>
                <prer:Identificacion>
                <prer:Nombre>{req.nombre_llegada}</prer:Nombre>
                </prer:Identificacion>
                
                <prer:DatosDireccion>
                <prer:Direccion>{req.direccion_llegada}</prer:Direccion>
                <prer:Localidad>{req.poblacion_llegada}</prer:Localidad>
                <prer:Provincia>{req.poblacion_llegada}</prer:Provincia>
                </prer:DatosDireccion>
                
                <prer:CP>{req.codigos_destino}</prer:CP>
                <prer:Telefonocontacto>{req.telefono_llegada}</prer:Telefonocontacto>
                <prer:Email>{req.email_llegada}</prer:Email>
                <DatosSMS>
                <NumeroSMS>{req.telefono_llegada}</NumeroSMS>
                </DatosSMS>
            </prer:Destinatario>
            <prer:Envios>"""  
    
    #build all packages inside Envios
    for i in range(req.cantidad):
        packages = req.packageList[i]
        payloadPackages = f"""
                    <prer:Envio>
                        <prer:NumBulto>{i+1}</prer:NumBulto>
                        <prer:Pesos>
                            <prer:Peso>
                                <prer:TipoPeso>R</prer:TipoPeso>
                                <prer:Valor>{packages.peso}</prer:Valor>
                            </prer:Peso>
                        </prer:Pesos>
                        <prer:Largo>{packages.largo}</prer:Largo>
                        <prer:Alto>{packages.alto}</prer:Alto>
                        <prer:Ancho>{packages.ancho}</prer:Ancho>
                        <Observaciones1>{packages.observaciones_salida}</Observaciones1>
                    </prer:Envio>                        
                """
        payloadB += payloadPackages

    payload2 += payloadB + f"""
            </prer:Envios>  
            <prer:CodProducto>S0132</prer:CodProducto>
            <prer:ModalidadEntrega>ST</prer:ModalidadEntrega>
            <prer:TipoFranqueo>FP</prer:TipoFranqueo>
            </prer:PreregistroEnvioMultibulto>   """    
    payload3 = f"""
        </soapenv:Body>
    </soapenv:Envelope>"""

    # Cabeceras
    headers = {
        'Content-Type': 'text/xml; charset=UTF-8'
    }

    # Request
    #print(payload+payload2+payload3)
    response = requests.post( url = url, headers=headers, auth=auth, data=(payload+payload2+payload3).encode("utf-8"))
    contesta = (response.text)
    #print('Response: ',response)
    #print('Contesta: ',contesta)

    contesta_dict = xmltodict.parse(contesta)

    bulto = contesta_dict['soapenv:Envelope']['soapenv:Body']['RespuestaPreregistroEnvioMultibulto']['Bultos']['Bulto']

    devuelve = PreRegister_Response(
        resultado = contesta_dict['soapenv:Envelope']['soapenv:Body']['RespuestaPreregistroEnvioMultibulto']['Resultado'],
        codExpedicion = contesta_dict['soapenv:Envelope']['soapenv:Body']['RespuestaPreregistroEnvioMultibulto']['CodExpedicion'],
        fechaRespuesta = contesta_dict['soapenv:Envelope']['soapenv:Body']['RespuestaPreregistroEnvioMultibulto']['FechaRespuesta'],
        bultos = [PreRegister_Response_Package(
            numBulto = b['NumBulto'], 
            codEnvio = b['CodEnvio'], 
            codManifiesto = b['CodManifiesto'], 
            ficheiro = PreRegister_Response_File(nombreFicheiro=b['Etiqueta']['Etiqueta_pdf']['NombreF'],
                                               tipoDoc=b['Etiqueta']['Etiqueta_pdf']['Tipo_Doc'],
                                               ficheiroBinario=b['Etiqueta']['Etiqueta_pdf']['Fichero']
        )) for b in bulto]
    )
    # print(payload+payload2+payload3)
    #print('Resultado:',devuelve.resultado, ', codExpedicion:', devuelve.codExpedicion, ', fechaRespuesta:',devuelve.fechaRespuesta, ', numBultos:',len(devuelve.bultos))
    return devuelve

@app.post("/Pickup")
async def pickup_correos (req: Shipment):

    if req.prod == 0:
        auth = PICKUP_PRE_AUTH
        url = PICKUP_PRE_URL
        contract = "99999999"
        detallable = "99999999"
        Annex = "091"
    else:
        auth = PICKUP_AUTH
        url = PICKUP_URL

    # Cabeceras
    headers = {
        'Content-Type': 'text/xml; charset=UTF-8'
    }
    payload = f""""""

    #response = requests.post(url=url, auth=auth, headers=headers data=payload)


@app.post("/ReqStatus")
async def reqstatus_correos (req: Shipment):
    
    url = ""