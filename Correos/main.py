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

# from correos_preregistro.vars import PRE_URL, URL
# from correos_preregistro.client import RawClient as Client
# from correos_preregistro.requests.preregistro_envio import  as Client
# from correos_preregistro.resources import Package, Receiver, Sender
from vars import PRE_URL, URL

import xml.etree.ElementTree as ET
from datetime import datetime

null = 'null'
false = False

class back(BaseModel):
    servicio: str
    id_usuario: str


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
    webservice: str
    client_uid: str
    pickup_from: Optional[str] = None
    pickup_until: Optional[str] = None
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
    fecha_recogida: str
    fecha_entrega: Optional[str] = None
    nombre_llegada: str
    nombre_salida: str
    packageList: List[Package]
    user: str
    password: str

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
    


@app.post("/shipment_create_correos")
async def shipment_create_correos(req: Shipment):

    # URL CORREOS
    url = (PRE_URL if req.prod == 0 else URL)#+"?wsdl"
    print('URL: ',url)
    
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
    if (req.webservice == 'shipment'):
        #setup the first part of the shipment info (addresses and contacts)
        payloadB = f"""
            <prer:PreregistroEnvioMultibulto>
                <prer:FechaOperacion>{req.fecha_recogida}</prer:FechaOperacion>
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
        print(req.cantidad)
        for i in range(req.cantidad):
            print('Current doc', i)
            packages = req.packageList[i]
            #print(packages)
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
                <prer:EntregaParcial></prer:EntregaParcial>
                    <prer:CodProducto>S0132</prer:CodProducto>
                    <prer:ReferenciaExpedicion></prer:ReferenciaExpedicion>
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
    print(payload+payload2+payload3)
    response = requests.post( url = url, headers=headers, auth=(req.user, req.password), data=(payload+payload2+payload3).encode("utf-8"))
    contesta = (response.text)
    print('Response: ',response)
    print('Contesta: ',contesta)

    # Parsing
    contesta_dict = xmltodict.parse(contesta)

    # print(contesta_dict) 


    # Resultados
    if(req.webservice == 'shipment'):
        resultado_dict = contesta_dict['soap:Envelope']['soap:Body']['GrabaServiciosResponse']['GrabaServiciosResult']['Servicios']['Envio']['Resultado']['@return']
        if resultado_dict == '0':
            codigo_envio = contesta_dict['soap:Envelope']['soap:Body']['GrabaServiciosResponse']['GrabaServiciosResult']['Servicios']['Envio']['@codexp'] 
            etiqueta = contesta_dict['soap:Envelope']['soap:Body']['GrabaServiciosResponse']['GrabaServiciosResult']['Servicios']['Envio']['Etiquetas']['Etiqueta']['#text']
            if req.id_agencia == "":
                agencia = "329"
            else:
                agencia = req.id_agencia
            devuelve = {'resultado': '1', "codigo_envio": codigo_envio, "codigo_recogida": codigo_envio, "id_agencia": agencia, "etiqueta": etiqueta}
        else:
            devuelve = {'resultado': "0", "codigo_envio": resultado_dict, "codigo_recogida": contesta_dict['soap:Envelope']['soap:Body']['GrabaServiciosResponse']['GrabaServiciosResult']['Servicios']['Envio']['Errores']['Error']}


    # print(payload+payload2+payload3)
    return devuelve