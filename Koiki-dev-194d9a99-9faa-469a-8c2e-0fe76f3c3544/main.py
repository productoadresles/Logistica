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
true = True

class ReqShipmentCreate(BaseModel):
    prod: int
    nombre_salida: str
    codigos_origen: str
    poblacion_salida: str
    iso_pais_salida: str
    direccion_salida: str
    email_salida: str
    nombre_llegada: str
    telefono_salida: str
    codigos_destino: str
    poblacion_llegada: str
    iso_pais_llegada: str
    direccion_llegada: str
    telefono_llegada: str
    email_llegada: str
    peso: int
    servicio: int
    cantidad_reembolso: Optional[int] = None
    observaciones_salida: Optional[str] = None
    fecha_recogida: str

class ReqStatus(BaseModel):
    prod: int
    codigo_envio: str
    codigos_destino: str


app = FastAPI()

handler = Mangum(app)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Llamadas DHL

@app.post("/shipment_create_koiki")
async def shipment_create_koiki(req: ReqShipmentCreate):
            
    # URLs
    url_pruebas = "https://rekistest.koiki.es/services/rekis/api/altaEnvios"
    url_producc = "https://rekis.koiki.es/services/rekis/api/altaEnvios"

    def random_with_N_digits(n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return random.randint(range_start, range_end)
 
    num_serie = random_with_N_digits(5)
    referencia = "adl"+str(num_serie)

    print(referencia)

    token_pre = "c4b5e506-def7-4fbf-a9d9-5a47c4c4e460"
    token_pro = "f922675d-59c8-476e-8d86-97443e97fae5"

    if req.prod == 0:
        token = token_pre
        url_envio = url_pruebas
    else:
        token = token_pro
        url_envio = url_producc

    
    
    payload = {"token":token, "formatoEtiqueta":"PDF", "envios": [{"nombreRemi":req.nombre_salida, "direccionRemi":req.direccion_salida, "codPostalRemi":req.codigos_origen, "poblacionRemi":req.poblacion_salida, "provinciaRemi":req.poblacion_salida, "paisRemi":req.iso_pais_salida, "emailRemi":req.email_salida, "telefonoRemi":req.telefono_salida, "nombreDesti":req.nombre_llegada, "direccionDesti":req.direccion_llegada, "codPostalDesti":req.codigos_destino, "poblacionDesti":req.poblacion_llegada, "provinciaDesti":req.poblacion_llegada, "paisDesti":req.iso_pais_llegada, "emailDesti":req.email_llegada, "telefonoDesti":req.telefono_llegada, "numPedido":referencia, "kilos":req.peso, "tipoServicio":req.servicio, "reembolso":req.cantidad_reembolso, "observaciones":req.observaciones_salida, "devolucion":"", "tipoMercancia":"", "claveAduanaOrigen":"", "claveAduanaDestino":"", "valorDeclarado":"", "numPedidoOriginal":"", "fechaRecogida":req.fecha_recogida}]}

    #payload = {"token":token, "formatoEtiqueta":"PDF", "envios": [{"nombreRemi":req.nombre_salida, "direccionRemi":req.direccion_salida, "codPostalRemi":req.codigos_origen, "poblacionRemi":req.poblacion_salida, "paisRemi":req.iso_pais_salida, "emailRemi":req.email_salida, "telefonoRemi":req.telefono_salida, "nombreDesti":req.nombre_llegada, "direccionDesti":req.direccion_llegada, "codPostalDesti":req.codigos_destino, "poblacionDesti":req.poblacion_llegada, "paisDesti":req.iso_pais_llegada, "emailDesti":req.email_llegada, "telefonoDesti":req.telefono_llegada, "numPedido":referencia, "kilos":req.peso, "tipoServicio":req.servicio, "reembolso":req.cantidad_reembolso, "observaciones":req.observaciones_salida, "devolucion":"", "tipoMercancia":"", "claveAduanaOrigen":"", "claveAduanaDestino":"", "valorDeclarado":"", "numPedidoOriginal":"", "fechaRecogida":req.fecha_recogida}]}

    print(payload)

    headers = {
		"content-type": "application/json",
	}
    
    response = requests.request("POST", url_envio, json=payload, headers=headers)

    data = json.loads(response.text)
    

    contenido = data.get("mensaje")
    variable = data.get("envios")[0]
    etiqueta = variable.get("etiqueta")
    track_num = variable.get("codBarras")
    cp_destino = req.codigos_destino
    #url_track = variable.get("numPedido")
    #url_status = "https://f7f7hhjlbn5vjsi2iddbfsbyxm0jmwni.lambda-url.us-east-1.on.aws/status_koiki/"

    #response2 = {'resultado': "1","etiqueta": data_conv, "url rastreo":url_track, "número rastreo": track_num}
    
    #for line in data_conv:
    #    contenido = f"{line['content']}"
    url_rastreo = "https://backend.koiki.eu/webclientes/seguimiento?trackingId="+track_num+"&cp="+cp_destino
        
    if  contenido != "OK":
        response2 = {'resultado': "0", "url_rastreo":"", "numero_rastreo": "", "etiqueta": ""}
    else:
        response2 = {'resultado': "1", "url_rastreo": url_rastreo, "codigo_envio": track_num, "etiqueta": etiqueta}

    

    contesta = json.loads(response.text)
    print(payload)
    print(contesta)
    
    #return contesta
    #return variable
    return response2

@app.post("/status_koiki")
async def status_koiki(req: ReqStatus):


    # URLs
    url_pruebas = "https://test.koiki.eu/services/kis/api/v1/service/track/see"
    url_producc = "https://koiki.eu/services/kis/api/v1/service/track/see"

    cp_destino = req.codigos_destino

    token_pre = "c4b5e506-def7-4fbf-a9d9-5a47c4c4e460"
    token_pro = "f922675d-59c8-476e-8d86-97443e97fae5"

    if req.prod == 0:
        token = token_pre
        url_envio = url_pruebas
    else:
        token = token_pro
        url_envio = url_producc

    payload_track = {"token": token, "code": req.codigo_envio}

    headers = {
		"content-type": "application/json",
	}
    
    response = requests.request("POST", url_envio, json=payload_track, headers=headers)
    respuesta = json.loads(response.text)


    #contenido = respuesta.get("result")
    
    #variable2 = respuesta.get("Error")

    if  "error" in respuesta:
        final_resp = {
            "estado": "101",
            "nombre_estado": "CODE NOT FOUND",
            "codigo_recogida": "false",
            "web_seguimiento": "false"
            }
    else:
        variable = respuesta.get("result")[0]
        nombre_estado = variable.get("codEstado")
        estado = variable.get("code")
        track_num = variable.get("servicio")
        url_rastreo = "https://backend.koiki.eu/webclientes/seguimiento?trackingId="+track_num+"&cp="+cp_destino
        final_resp = {
            "estado": estado,
            "nombre_estado": nombre_estado,
            "codigo_envio": track_num,
            "web_seguimiento": url_rastreo
            }
    

    #logs
    print(payload_track)
    print(respuesta)
    print(final_resp)
    
    return final_resp