from typing import Optional
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

class ReqShipmentCreateEnvialia(BaseModel):
    prod: str
    peso: int
    bultos: int
    contenido: Optional[str] = None
    taric: Optional[str] = None
    valor: Optional[str] = None
    valor_mercancia: Optional[int] = None
    contenido_envio: Optional[str] = None
    contrareembolso: Optional[int] = None
    cantidad_reembolso: Optional[int] = None
    seguro: Optional[int] = None
    dia_laborable_automatico: Optional[int] = None
    importe_seguro: Optional[int] = None
    dropshipping: Optional[int] = None
    codigos_origen: str
    poblacion_salida: str
    iso_pais_salida: str
    direccion_salida: str
    email_salida: str
    nombre_salida: str
    telefono_salida: str
    codigos_destino: str
    poblacion_llegada: str
    iso_pais_llegada: str
    direccion_llegada: str
    telefono_llegada: Optional[str] = None
    email_llegada: str
    nombre_llegada: str
    dni_llegada: Optional[str] = None
    observaciones_salida: Optional[str] = None
    contacto_salida: Optional[str] = None
    observaciones_llegada: Optional[str] = None
    contacto_llegada: Optional[str] = None
    codigo_mercancia: Optional[str] = None
    cod_promo: Optional[str] = None
    fecha_recogida: str
    hora_recogida_desde: str
    hora_recogida_hasta: str

class ReqStatus(BaseModel):
    codigo_envio: str

app = FastAPI()

handler = Mangum(app)

@app.get("/")
async def root():
    return {"message": "API de Envialia"}

## 2023-03-24

def transformar_fecha(fecha_str):
    formato_entrada = "%d/%m/%Y"
    formato_salida = "%Y-%m-%d"

    fecha_dt = datetime.strptime(fecha_str, formato_entrada)
    fecha_nueva = fecha_dt.strftime(formato_salida)

    return fecha_nueva

@app.post("/shipment_create_envialia")
async def shipment_create_envialia(req: ReqShipmentCreateEnvialia):
    
    # URL Envialia
    #url2 = 'http://wstest.envialia.com:9085/soap'
    null = 'null'
    false = False

    # Variables para grabar servicio
    urlProd = 'http://ws.envialia.com/soap'
    urlPruebas = 'http://wstest.envialia.com:9085/soap'
    clienteProd = "863"
    clientePruebas = "WS001"
    agenciaProd = "004895"
    agenciaPruebas = "002800"
    passProd = "B09718495"
    passProdnew="adresles@2024"
    passPruebas = "Adresle2023"

    # Condición productivo
    if req.prod == "1":
        cliente = clienteProd
        agencia = agenciaProd
        url2 = urlProd
        passEnv = passProd
    else:
        cliente = clientePruebas
        agencia = agenciaPruebas
        url2 = urlPruebas
        passEnv = passPruebas

    # Cabeceras
    headers = {
        'Content-Type': 'text/xml; charset=UTF-8'
    }

    # Payloads
    def generar_codigo():
        caracteres = string.ascii_uppercase + string.digits
        codigo = ''.join(random.choice(caracteres) for i in range(10))
        return codigo

    RefC = generar_codigo()

    payload_login = f"""<?xml version="1.0" encoding="utf-8"?>
                        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                            <soap:Body>
                                <LoginWSService___LoginCli2>
                                    <strCodAge>{agencia}</strCodAge>
                                    <strCliente>{cliente}</strCliente>
                                    <strPass>{passEnv}</strPass>
                                </LoginWSService___LoginCli2>
                            </soap:Body>
                        </soap:Envelope>"""
    
    responseL = requests.post(url2, headers=headers, data=payload_login)

    #print(responseL)
    print(payload_login)
    print(responseL.text)
    # return response
    contesta = (responseL.text)
    contesta_dict = xmltodict.parse(contesta)
    uidss = contesta_dict["SOAP-ENV:Envelope"]["SOAP-ENV:Header"]["ROClientIDHeader"]["ID"]

    #fecha_recogida = transformar_fecha(req.fecha_recogida)
    
    payload_graba3 = f"""<?xml version="1.0" encoding="utf-8"?>
					<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
					<soap:Header>
						<ROClientIDHeader xmlns="http://tempuri.org/">
							<ID>{uidss}</ID>
						</ROClientIDHeader>
					</soap:Header>
					<soap:Body>
					<WebServService___GrabaRecogida3 xmlns="http://tempuri.org/">
						<strCod></strCod>
                        <strCodAgeOri></strCodAgeOri>
                        <strCodAgeDes></strCodAgeDes>
						<strCodAgeCargo>{agencia}</strCodAgeCargo>
						<dtFecRec>{req.fecha_recogida}</dtFecRec>
						<dtHoraRecIni>{req.fecha_recogida} 09:00:00</dtHoraRecIni>
                        <dtHoraRecIniTarde>{req.fecha_recogida} 16:00:00</dtHoraRecIniTarde>
						<dtHoraRecFin>{req.fecha_recogida} 14:00:00</dtHoraRecFin>
                        <dtHoraRecFinTarde>{req.fecha_recogida} 19:00:00</dtHoraRecFinTarde>
						<dPeso>{req.peso}</dPeso>
                        <intBul>{req.bultos}</intBul>
						<dValor>0</dValor>
						<strCodVeh></strCodVeh>
						<strNomOri>"{req.nombre_salida}"</strNomOri>
						<strDirOri>"{req.direccion_salida}"</strDirOri>..
						<strPobOri>"{req.poblacion_salida}"</strPobOri>
						<strCPOri>{req.codigos_origen}</strCPOri>
						<strTlfOri>{req.telefono_salida}</strTlfOri>
						<strNomDes>"{req.nombre_llegada}"</strNomDes>
						<strDirDes>"{req.direccion_llegada}"</strDirDes>
						<strPobDes>"{req.poblacion_llegada}"</strPobDes>
						<strCPDes>{req.codigos_destino}</strCPDes>
						<strTlfDes>{req.telefono_llegada}</strTlfDes>
						<strCodCli>{cliente}</strCodCli>
						<strPersContacto>"{req.nombre_salida}"</strPersContacto>
						<boAutKM>0</boAutKM>
						<strCodTipoServ>24</strCodTipoServ>
						<boSabado>0</boSabado>
						<strCodRep></strCodRep>
						<strCodEnv></strCodEnv>
						<strRef>{RefC}</strRef>
						<strTipoRecOld></strTipoRecOld>
						<dReembolso>0</dReembolso>
						<dCobCli>0</dCobCli>
						<dImpuesto>0</dImpuesto>
						<dBaseImp>0</dBaseImp>
						<boAcuse>0</boAcuse>
						<boRetorno>0</boRetorno>
						<boGestOri>0</boGestOri>
						<boGestDes>0</boGestDes>
						<strCodPais>34</strCodPais>
						<strRemMoviles>{req.telefono_salida}</strRemMoviles>
						<strRemDirEmails>{req.email_salida}</strRemDirEmails>
						<strCampo1></strCampo1>
						<strCampo2></strCampo2>
						<strCampo3></strCampo3>
						<strCampo4></strCampo4>
					</WebServService___GrabaRecogida3>
					</soap:Body>
				</soap:Envelope>"""
	
    responseG = requests.post(url2, headers=headers, data=payload_graba3)
    contesta_graba = (responseG.text)
    contesta_dict_graba = xmltodict.parse(contesta_graba)
 
	#fault = contesta_dict_graba["SOAP-ENV:Envelope"]["SOAP-ENV:Body"]["SOAP-ENV:Fault"]["faultcode"]
	#cod_reco = contesta_dict_graba["SOAP-ENV:Envelope"]["SOAP-ENV:Body"]["v1:WebServService___GrabaRecogida3Response"]["v1:strCodOut"]
	
    # Uso de texto porque hasta el momento no se ha econtrado una manera de ejecutar la condición
    status = contesta_graba[498:500]
	
    if status == 'v1':
        codigo_response = contesta_dict_graba["SOAP-ENV:Envelope"]["SOAP-ENV:Header"]["ROClientIDHeader"]["ID"][1:-1]
        web_seguimiento = f"""http://www.envialia.com/seguimiento/?t=r&v={RefC}&cp={req.codigos_destino}"""
        devuelve = {
                     "resultado": '1', 
                     "codigo_envio": RefC, 
                     "codigo_recogida": contesta_dict_graba["SOAP-ENV:Envelope"]["SOAP-ENV:Body"]["v1:WebServService___GrabaRecogida3Response"]["v1:strCodOut"],
                     "web_seguimiento": web_seguimiento 
                     }
    else:
        devuelve = {'resultado': "0", "codigo_envio": "", "codigo_recogida": ""}
	
    #return devuelve
    return contesta_dict_graba


def transform_status_response(texto):
     # Reemplazar las entidades HTML
    texto = texto.replace("&lt;", "<").replace("&gt;", ">")

    # Analizar el texto XML
    raiz = ET.fromstring(texto)

    # Extraer los elementos ENV_ESTADOS_REF
    elementos = raiz.findall("ENV_ESTADOS_REF")

    # Crear la lista de diccionarios
    lista_diccionarios = []

    for elemento in elementos:
        diccionario = {}
        for atributo, valor in elemento.attrib.items():
            diccionario[atributo] = valor
        lista_diccionarios.append(diccionario)

    return lista_diccionarios


@app.post("/status_envialia")
async def status_envialia(req_track: ReqStatus):


	# URL
    url2 = 'http://ws.envialia.com/soap'
    urlProd = 'http://ws.envialia.com/soap'
    #urlPruebas = 'http://wstest.envialia.com:9085/soap'
    clienteProd = "863"
    #clientePruebas = "WS001"
    agenciaProd = "004895"
    #agenciaPruebas = "002800"
    passProd = "B09718495"
    #passPruebas = "Adresle2023"
	
	# Cabeceras
    headers = {
		'Content-Type': 'text/xml; charset=UTF-8'
	}
	
	# Payloads
	

	# Payloads
	
    payload_login2 = f"""<?xml version="1.0" encoding="utf-8"?>
                    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
                    	<soap:Body>
                    		<LoginWSService___LoginCli2>
                    			<strCodAge>{agenciaProd}</strCodAge>
                    			<strCliente>{clienteProd}</strCliente>
                    			<strPass>{passProd}</strPass>
                    		</LoginWSService___LoginCli2>
                    	</soap:Body>
                    </soap:Envelope>"""
                    
	
    responseL = requests.post(url2, headers=headers, data=payload_login2)

	#print(responseL)
	#print(responseL.text)
	#return response
    contesta = (responseL.text)
    contesta_dict = xmltodict.parse(contesta)
    uidssLog = contesta_dict["SOAP-ENV:Envelope"]["SOAP-ENV:Header"]["ROClientIDHeader"]["ID"]
                    
    
	
    
    payload_track3 = f"""<?xml version="1.0" encoding="utf-8"?>
					<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
					<soap:Header>
						<ROClientIDHeader xmlns="http://tempuri.org/">
							<ID>{uidssLog}</ID>
						</ROClientIDHeader>
					</soap:Header>
					<soap:Body>
					<WebServService___ConsEnvEstadosRef>
						<strRef>{req_track.codigo_envio}</strRef>
					</WebServService___ConsEnvEstadosRef>
					</soap:Body>
				</soap:Envelope>"""

    responseTrack = requests.post(urlProd, headers=headers, data=payload_track3)
    contesta_track = (responseTrack.text)
    contesta_dict_track = xmltodict.parse(contesta_track)
    texto = contesta_dict_track["SOAP-ENV:Envelope"]["SOAP-ENV:Body"]["v1:WebServService___ConsEnvEstadosRefResponse"]["v1:strEnvEstadosRef"]

    list_status = transform_status_response(texto)
    
    ultimo_elemento = list_status[-1]
    valor = ultimo_elemento["V_COD_TIPO_EST"]

    list_status.reverse()

    response = {
         "codigo_envio": req_track.codigo_envio,
         "estado": valor,
         "historico": list_status
    }

    return response