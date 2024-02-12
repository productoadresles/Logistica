import urllib.request
import urllib.parse
import re
import requests
import xmltodict
import json
import xml.etree.ElementTree as ET
from typing import Optional
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum
from datetime import datetime

null = 'null'
false = False

class ReqShipmentCreate(BaseModel):
    prod: str
    fecha_recogida: str
    bultos:int
    peso: str
    nombre_origen: str
    direc_origen: str
    cp_origen: str
    tel_origen: str
    nombre_dest: str
    direc_dest: str
    cp_dest: str
    tel_dest: str
    observaciones: str
    poblacion_ori: str
    poblacion_dest:str

class ReqStatus(BaseModel):
    codigo_envio: str

app = FastAPI()

handler = Mangum(app)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Llamadas Envíos Perros 

@app.post("/shipment_create_tipsa")
async def shipment_create_tipsa(req: ReqShipmentCreate):
    
    # URLs
    url_login_test = "http://79.171.110.38:8097/SOAP?service=LoginWSService"
    url_login_prod = "http://webservices.tipsa-dinapaq.com/SOAP?service=LoginWSService"
    url_accion_test = "http://79.171.110.38:8097/SOAP?service=WebServService"
    url_accion_prod = "http://webservices.tipsa-dinapaq.com/SOAP?service=WebServService"

    # Cabeceras
    headers = {
        'Content-Type': 'text/xml; charset=UTF-8'
    }

    # Login
    payload_login = f"""<?xml version="1.0" encoding="utf-8"?>
                    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
                        <soapenv:Header>
                            <tem:ROClientIDHeader>
                                <tem:ID></tem:ID>
                            </tem:ROClientIDHeader>
                        </soapenv:Header>
                        <soapenv:Body>
                            <tem:LoginWSService___LoginCli>
                                <tem:strCodAge>000000</tem:strCodAge>
                                <tem:strCod>33333</tem:strCod>
                                <tem:strPass>Pr%20#23%</tem:strPass>
                            </tem:LoginWSService___LoginCli>
                        </soapenv:Body>
                    </soapenv:Envelope>"""
    
    response_login = requests.post( url = url_login_test, headers=headers, data=payload_login)
    print(response_login.text)
    contesta_login = (response_login.text)

    # Obtener UID
    contesta_dict = xmltodict.parse(contesta_login)

    resultado_dict = contesta_dict['SOAP-ENV:Envelope']['SOAP-ENV:Body']['v1:LoginWSService___LoginCliResponse']['v1:Result']
    sesion = contesta_dict['SOAP-ENV:Envelope']['SOAP-ENV:Body']['v1:LoginWSService___LoginCliResponse']['v1:strSesion']

    print(resultado_dict)
    print(sesion)


    # Creación envío

    payload_envio = f"""<?xml version="1.0" encoding="utf-8"?>
                    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                        <soap:Header>
                            <ROClientIDHeader xmlns="http://tempuri.org/">
                                <ID>{sesion}</ID>
                            </ROClientIDHeader>
                        </soap:Header>
                        <soap:Body>
                            <WebServService___GrabaEnvio24 xmlns="http://tempuri.org/">
                                <strCodAgeCargo>000000</strCodAgeCargo>
                                <strCodAgeOri>000000</strCodAgeOri>
                                <strCodCli>33333</strCodCli>
                                <strRef>ABCD</strRef>
                                <dtFecha>{req.fecha_recogida}</dtFecha>
                                <strCodTipoServ>48</strCodTipoServ>
                                <strCPDes>{req.cp_dest}</strCPDes>
                                <strPobDes>{req.poblacion_dest}</strPobDes>
                                <strNomDes>{req.nombre_dest}</strNomDes>
                                <strTlfDes>{req.tel_dest}</strTlfDes>
                                <strDirDes>{req.direc_dest}</strDirDes>
                                <strCPOri>{req.cp_origen}</strCPOri>
                                <strPobOri>{req.poblacion_ori}</strPobOri>
                                <strNomOri>{req.nombre_origen}</strNomOri>
                                <strTlfOri>{req.tel_origen}</strTlfOri>
                                <strDirOri>{req.direc_origen}</strDirOri>
                                <dPesoOri>{req.peso}</dPesoOri>
                                <intPaq>{req.bultos}</intPaq>
                                <strObs>{req.observaciones}</strObs>
                                <boInsert>true</boInsert>
                                <strEtiquetaOut>PDF</strEtiquetaOut>
                            </WebServService___GrabaEnvio24>
                        </soap:Body>
                    </soap:Envelope>"""

    response_envio = requests.post( url = url_accion_test, headers=headers, data=payload_envio)
    print(response_envio.text)
    contesta_envio = (response_envio.text)

    contesta_albaran = xmltodict.parse(contesta_envio)

    albaran = contesta_albaran['SOAP-ENV:Envelope']['SOAP-ENV:Body']['v1:WebServService___GrabaEnvio24Response']['v1:strAlbaranOut']


    url_envio = "https://aplicaciones.tip-sa.com/cliente/datos_env.php?id="+"000000000000"+albaran

    # Etiqueta
    
    payload_etiqueta = f"""<?xml version="1.0" encoding="utf-8"?>
                    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                        <soap:Header>
                            <ROClientIDHeader xmlns="http://tempuri.org/">
                                <ID>{sesion}</ID>
                            </ROClientIDHeader>
                        </soap:Header>
                        <soap:Body>
                            <WebServService___ConsEtiquetaEnvio8>
                                <strCodAgeOri>000000</strCodAgeOri>
                                <strCodAgeCargo>000000</strCodAgeCargo>
                                <strAlbaran>{albaran}</strAlbaran>
                                <intIdRepDet>0</intIdRepDet>
                                <strFormato>pdf</strFormato>
                            </WebServService___ConsEtiquetaEnvio8>
                        </soap:Body>
                    </soap:Envelope>"""
    
    response_etiqueta = requests.post( url = url_accion_test, headers=headers, data=payload_etiqueta)
    print(response_etiqueta.text)
    contesta_etiqueta = (response_etiqueta.text)

    contesta_etiqueta_pdf = xmltodict.parse(contesta_etiqueta)

    etiqueta = contesta_etiqueta_pdf['SOAP-ENV:Envelope']['SOAP-ENV:Body']['v1:WebServService___ConsEtiquetaEnvio8Response']['v1:strEtiqueta']

    # Respuesta
    
    devuelve = {'resultado': '1', "codigo_envio": albaran, "url_seguimiento_envio": url_envio, "etiqueta": etiqueta}
    
    return devuelve


@app.post("/status_tipsa")
async def shipment_create_tipsa(req: ReqStatus):
    
    # URLs
    url_login_test = "http://79.171.110.38:8097/SOAP?service=LoginWSService"
    url_login_prod = "http://webservices.tipsa-dinapaq.com/SOAP?service=LoginWSService"
    url_accion_test = "http://79.171.110.38:8097/SOAP?service=WebServService"
    url_accion_prod = "http://webservices.tipsa-dinapaq.com/SOAP?service=WebServService"

    # Cabeceras
    headers = {
        'Content-Type': 'text/xml; charset=UTF-8'
    }

    # Login
    payload_login = f"""<?xml version="1.0" encoding="utf-8"?>
                    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
                        <soapenv:Header>
                            <tem:ROClientIDHeader>
                                <tem:ID></tem:ID>
                            </tem:ROClientIDHeader>
                        </soapenv:Header>
                        <soapenv:Body>
                            <tem:LoginWSService___LoginCli>
                                <tem:strCodAge>000000</tem:strCodAge>
                                <tem:strCod>33333</tem:strCod>
                                <tem:strPass>Pr%20#23%</tem:strPass>
                            </tem:LoginWSService___LoginCli>
                        </soapenv:Body>
                    </soapenv:Envelope>"""
    
    response_login = requests.post( url = url_login_test, headers=headers, data=payload_login)
    print(response_login.text)
    contesta_login = (response_login.text)

    # Obtener UID
    contesta_dict = xmltodict.parse(contesta_login)

    resultado_dict = contesta_dict['SOAP-ENV:Envelope']['SOAP-ENV:Body']['v1:LoginWSService___LoginCliResponse']['v1:Result']
    sesion = contesta_dict['SOAP-ENV:Envelope']['SOAP-ENV:Body']['v1:LoginWSService___LoginCliResponse']['v1:strSesion']

    print(resultado_dict)
    print(sesion)

    # Consultar envío

    payload_seguimiento = f"""<?xml version="1.0" encoding="utf-8"?>
                    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                        <soap:Header>
                            <ROClientIDHeader xmlns="http://tempuri.org/">
                                <ID>{sesion}</ID>
                            </ROClientIDHeader>
                        </soap:Header>
                        <soap:Body>
                            <WebServService___ConsEnvio>
                                <strCodAgeCargo>000000</strCodAgeCargo>
                                <strCodAgeOri>000000</strCodAgeOri>
                                <strAlbaran>{req.codigo_envio}</strAlbaran>
                            </WebServService___ConsEnvio>
                        </soap:Body>
                    </soap:Envelope>"""
    
    payload_seguimiento2 = f"""<?xml version="1.0" encoding="utf-8"?>
                    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                        <soap:Header>
                            <ROClientIDHeader xmlns="http://tempuri.org/">
                                <ID>{sesion}</ID>
                            </ROClientIDHeader>
                        </soap:Header>
                        <soap:Body>
                            <WebServService___ConsEnvEstados>
                                <strCodAgeCargo>000000</strCodAgeCargo>
                                <strCodAgeOri>000000</strCodAgeOri>
                                <strAlbaran>{req.codigo_envio}</strAlbaran>
                            </WebServService___ConsEnvEstados>
                        </soap:Body>
                    </soap:Envelope>"""
    
    response_seguimiento = requests.post( url = url_accion_test, headers=headers, data=payload_seguimiento2)
    print(response_seguimiento.text)
    contesta_seguimiento = (response_seguimiento.text)

    contesta_seguimiento_data = xmltodict.parse(contesta_seguimiento)

    resultado_seguimiento = contesta_seguimiento_data['SOAP-ENV:Envelope']['SOAP-ENV:Body']['v1:WebServService___ConsEnvEstadosResponse']['v1:strEnvEstados']

    url_envio = "https://aplicaciones.tip-sa.com/cliente/datos_env.php?id="+"000000000000"+req.codigo_envio

    devuelve_seguimiento = {"info_seguimiento": resultado_seguimiento, "web_seguimiento": url_envio}

    return devuelve_seguimiento