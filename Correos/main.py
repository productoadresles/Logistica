from typing import Optional
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum
import random
import string

import requests
import json
import xml.dom.minidom
import xmltodict
import unicodedata

import xml.etree.ElementTree as ET
from datetime import datetime

null = 'null'
false = False

class back(BaseModel):
    servicio: str
    id_usuario: str


class paquete2(BaseModel):
    pickup_from: Optional[str] = None
    pickup_until: Optional[str] = None
    codigos_origen: str
    codigos_destino: str
    direccion_salida: str
    direccion_llegada: str
    email_llegada: str
    email_salida: str
    fecha_recogida: str
    fecha_entrega: Optional[str] = None
    nombre_llegada: str
    nombre_salida: str
    observaciones_llegada: Optional[str] = None
    observaciones_salida: Optional[str] = None
    peso: int
    poblacion_llegada: str
    poblacion_salida: str
    telefono_llegada: Optional[str] = None
    telefono_salida: str

class paqueteList(BaseModel):
    id_agencia: str
    prod: int
    cantidad: int
    webservice: str
    client_uid: str
    paquete: List[paquete2]

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
async def shipment_create_correos(req: paqueteList):
        
    # URL GLS
    url = "https://wsclientes.asmred.com/b2b.asmx?wsdl"

    


    #  Generación de la referencia tipo C
    def random_with_N_digits(n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return random.randint(range_start, range_end)

    payload = f"""<?xml version="1.0" encoding="utf-8"?>
                    <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
                    <soap12:Body>
                    <GrabaServicios  xmlns="http://www.asmred.com/">
                    <docIn>
                        <Servicios uidcliente="{req.client_uid}" xmlns="http://www.asmred.com/">"""                       
    if (req.webservice == 'shipment'):
        i = 0
        while i <= req.cantidad:
            b = 0
            payloadB = f""""""
            results = req.paquete[b]
            
            payload2 = f"""     
                        <Envio codbarras="">
                            <Fecha dia="{results.fecha_recogida}">
                            </Fecha>
                            <FechaPrevistaEntrega>
                            </FechaPrevistaEntrega>
                            <Portes>P</Portes>
                            <Servicio>1</Servicio>
                            <Horario>2</Horario>
                            <Bultos>1</Bultos>
                            <Peso>{results.peso}</Peso>
                            <Retorno>0</Retorno>
                            <Pod>N</Pod>
                            <Remite>
                                <Plaza></Plaza>
                                <Nombre>{results.nombre_salida}</Nombre>
                                <Direccion>{results.direccion_salida}</Direccion>
                                <Poblacion>{results.poblacion_salida}</Poblacion>
                                <Provincia>{results.poblacion_salida}</Provincia>
                                <Pais>34</Pais>
                                <CP>{results.codigos_origen}</CP>
                                <Telefono>{results.telefono_salida}</Telefono>
                                <Movil></Movil>
                                <Email>{results.email_salida}</Email>
                                <Observaciones>{results.observaciones_salida}</Observaciones>
                            </Remite>
                            <Destinatario>
                                <Codigo></Codigo>
                                <Plaza></Plaza>
                                <Nombre>{results.nombre_llegada}</Nombre>
                                <Direccion>{results.direccion_llegada}</Direccion>
                                <Poblacion>{results.poblacion_llegada}</Poblacion>
                                <Provincia>{results.poblacion_llegada}</Provincia>
                                <Pais>34</Pais>
                                <CP>{results.codigos_destino}</CP>
                                <Telefono>{results.telefono_llegada}</Telefono>
                                <Movil>{results.telefono_llegada}</Movil>
                                <Email>{results.email_llegada}</Email>
                                <Observaciones>{results.observaciones_llegada}</Observaciones>
                                <ATT>{results.nombre_llegada}</ATT>
                            </Destinatario>
                            <Referencias>
                                <DevuelveAdicionales>
                                        <Etiqueta tipo="PDF"></Etiqueta>
                                </DevuelveAdicionales>
                            </Referencias>
                        </Envio>"""
            payloadB += payload2
            b = b+1
            i = i+1
 
    if (req.webservice == 'pickup'):                     
        i = 0
        while i <= req.cantidad:
            b = 0
            payloadB = f""""""
            results = req.paquete[b]
            print(results)
            payload2 = f"""     
                        <Recogida codrecogida="">
                            <Horarios>
                                <Fecha dia="{results.fecha_recogida}">
                                    <Horario desde="{results.pickup_from}" hasta="{results.pickup_until}" />
                                </Fecha>
                            </Horarios>
                            <RecogerEn>
                                <Nombre>{results.nombre_salida}</Nombre>
                                <Direccion>{results.direccion_salida}</Direccion>
                                <Poblacion>{results.poblacion_salida}</Poblacion>
                                <Pais>34</Pais>
                                <CP>{results.codigos_origen}</CP>
                                <Telefono>{results.telefono_salida}</Telefono>
                                <Email>{results.email_salida}</Email>
                                <Observaciones>{results.observaciones_salida}</Observaciones>
                                <Contacto></Contacto>
                            </RecogerEn>
                            <DevuelveAdicionales>
                                <Etiqueta tipo="PDF"></Etiqueta>
                            </DevuelveAdicionales>
                            <Entregas>
                                <Envio>
                                    <FechaPrevistaEntrega>
                                        <Fecha dia="{results.fecha_entrega}">
                                            <Horario desde="10:00" hasta="16:00" />
                                        </Fecha>
                                    </FechaPrevistaEntrega>
                                    <Portes>P</Portes>
                                    <Servicio>1</Servicio>
                                    <Horario>2</Horario>
                                    <Bultos>1</Bultos>
                                    <Peso>{results.peso}</Peso>
                                    <Retorno>0</Retorno>
                                    <Pod>N</Pod>
                                    <Destinatario>
                                        <Nombre>{results.nombre_llegada}</Nombre>
                                        <Direccion>{results.direccion_llegada}</Direccion>
                                        <Poblacion>{results.poblacion_llegada}</Poblacion>
                                        <Pais>34</Pais>
                                        <CP>{results.codigos_destino}</CP>
                                        <Telefono>{results.telefono_llegada}</Telefono>
                                        <Movil>{results.telefono_llegada}</Movil>
                                        <Email>{results.email_llegada}</Email>
                                        <Observaciones>{results.observaciones_llegada}</Observaciones>
                                        <ATT>{results.nombre_llegada}</ATT>
                                    </Destinatario>
                                </Envio>
                            </Entregas>
                        </Recogida>"""
            payloadB += payload2
            b = b+1
            i = i+1    
    
    
    payload3 = f"""     </Servicios>
                        </docIn>
                    </GrabaServicios>
                    </soap12:Body>
                    </soap12:Envelope>"""

    # Cabeceras
    headers = {
        'Content-Type': 'text/xml; charset=UTF-8'
    }

    # Request
    print(payload+payload2+payload3)
    response = requests.post( url = url, headers=headers, data=payload+payload2+payload3)
    contesta = (response.text)
    # print(response)

    # Parsing
    contesta_dict = xmltodict.parse(contesta)

    # print(contesta_dict) 


    # Resultados
    if(req.webservice == 'pickup'):
        resultado_dict = contesta_dict['soap:Envelope']['soap:Body']['GrabaServiciosResponse']['GrabaServiciosResult']['Servicios']['Recogida']['Resultado']['@return']
        if resultado_dict == '0':
            codigo_recogida = contesta_dict['soap:Envelope']['soap:Body']['GrabaServiciosResponse']['GrabaServiciosResult']['Servicios']['Recogida']['@codigo']
            etiqueta = contesta_dict['soap:Envelope']['soap:Body']['GrabaServiciosResponse']['GrabaServiciosResult']['Servicios']['Recogida']['Etiquetas']['Etiqueta']['#text']
            if req.id_agencia == "":
                agencia = "329"
            else:
                agencia = req.id_agencia
            devuelve = {'resultado': '1', "codigo_envio": 0, "codigo_recogida": codigo_recogida, "id_agencia": agencia, "etiqueta": etiqueta}
        else:
            devuelve = {'resultado': "0", "codigo_envio": resultado_dict, "codigo_recogida": contesta_dict['soap:Envelope']['soap:Body']['GrabaServiciosResponse']['GrabaServiciosResult']['Servicios']['Recogida']['Errores']['Error']}

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


@app.post("/status_correos")
async def status_correos(request: ReqStatus):
    
    
    # URL GLS
    url = "https://wsclientes.asmred.com/b2b.asmx?wsdl"

    # Variables para grabar servicio
    uidClienteProd = "d0cceea3-15a4-428e-9754-cd17777de34f"
    uidClientePruebas = "6BAB7A53-3B6D-4D5A-9450-702D2FAC0B11"
    uidAgencia815 = "8412161e-a861-4ba4-9060-087f4c14078c"
    uidAgencia214 = "4f7845c1-8e91-4b76-92de-9cc0d59ea1d9"

    # if (request.prod == 1):
    #     if (request.id_agencia == ""):
    #         uid = uidClienteProd
    #     if (request.id_agencia == "329"):
    #         uid = uidClienteProd
    #     if (request.id_agencia == "gls815"):
    #         uid = uidAgencia815
    #     if (request.id_agencia == "gls214"):
    #         uid = uidAgencia214
    # else:
    #     uid = uidClientePruebas

    # if (request.prod == 1):
    #     if (request.id_agencia == ""):
    #         uid = uidClienteProd
    #     if (request.id_agencia == "gls329" or request.id_agencia == "329"):
    #         uid = uidClienteProd
    #     if (request.id_agencia == "gls815" or request.id_agencia == "815"):
    #         uid = uidAgencia815
    #     if (request.id_agencia == "gls214" or request.id_agencia == "214"):
    #         uid = uidAgencia214
    # else:
    #     uid = uidClientePruebas
    
    # Orden XML

    payload_rastrear = f"""<?xml version="1.0" encoding="utf-8"?>
                    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns="http://www.asmred.com/"><soap:Header/>
                    <soap:Body>
                        <GetExpCli>
                            <codigo>{request.codigo_recogida}</codigo>
                            <uid>{request.client_uid}</uid>
                        </GetExpCli>
                    </soap:Body>
                    </soap:Envelope>"""

    # Cabeceras
    headers = {
        'Content-Type': 'text/xml; charset=UTF-8'
    }
    
    
    response = requests.post(url, headers=headers, data=payload_rastrear)

    contesta = (response.text)

    contesta_dict = xmltodict.parse(contesta)
    
    if "exp" in contesta_dict["soap:Envelope"]["soap:Body"]["GetExpCliResponse"]["GetExpCliResult"]["expediciones"]:
        cp_destino = contesta_dict["soap:Envelope"]["soap:Body"]["GetExpCliResponse"]["GetExpCliResult"]["expediciones"]["exp"]["cp_dst"]
        codexp = contesta_dict["soap:Envelope"]["soap:Body"]["GetExpCliResponse"]["GetExpCliResult"]["expediciones"]["exp"]["codexp"]
        web_seguimiento = f"""https://m.gls-spain.es/e/{codexp}/{cp_destino}"""
        respuesta = {
            "estado": contesta_dict['soap:Envelope']['soap:Body']['GetExpCliResponse']['GetExpCliResult']['expediciones']['exp']['codestado'],
            "nombre_estado": contesta_dict['soap:Envelope']['soap:Body']['GetExpCliResponse']['GetExpCliResult']['expediciones']['exp']['estado'],
            "codigo_recogida": request.codigo_recogida,
            "web_seguimiento": web_seguimiento
            }
    else:
        respuesta = {
            "estado": "0",
            "nombre_estado": "not created",
            "codigo_recogida": "false",
            "web_seguimiento": "false"
            }

    print(payload_rastrear)
    print(contesta_dict)
    return respuesta
    #return contesta