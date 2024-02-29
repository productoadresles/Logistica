import urllib.request
import urllib.parse
import re
import requests
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
    deliveryType: str
    prod: str
    fecha_recogida: str
    hora_recogida_desde: str
    deliveryType: str
    type: str
    depth: str
    width: str
    height: str
    weight: str
    #description: str
    #descripcion_producto: str
    #valor_mercancia: str
    street_origin: str
    interior_number_origin: str
    outdoor_number_origin: str
    zip_code_origin: str
    neighborhood_origin: str
    city_origin: str
    state_origin: str
    references_origin: str
    name_origin: str
    email_origin: str
    phone_origin: str
    rfc_origin: str
    street_dest: str
    interior_number_dest: str
    outdoor_number_dest: str
    zip_code_dest: str
    neighborhood_dest: str
    city_dest: str
    state_dest: str
    references_dest: str
    name_dest: str
    email_dest: str
    phone_dest: str
    rfc_dest: str
    claveProdServ: str
    description: str
    value: str
    
class ReqStatus(BaseModel):
    codigo_envio: str

app = FastAPI()

handler = Mangum(app)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Llamadas Envíos Perros 

@app.post("/shipment_create_envios_perros")
async def shipment_create_envios_perros(req: ReqShipmentCreate):
    
    # orders
    
    if(req.prod == '1'):
        url_orders = "https://app.enviosperros.com/api/v2/orders"
        url_mock_guide_pruebas = "https://app.enviosperros.com/api/v2/guide/order"
        url_mock_pickup_pruebas = "https://app.enviosperros.com/api/v2/pickup"
        headers = {
            'Authorization': 'Bearer Dh2vxj1C4Mclp1Op26ifaBRoGfQ3frCsWCFDgYMG',
            'Content-Type': 'application/json'
        }  
         
    
    elif (req.prod == "0"): 
        url_orders = "https://staging-app.enviosperros.com/api/v2/orders"
        url_mock_guide_pruebas = "https://staging-app.enviosperros.com/api/v2/guide/order"
        url_mock_pickup_pruebas = "https://staging-app.enviosperros.com/api/v2/pickup"
        headers = {
            'Authorization': 'Bearer Dh2vxj1C4Mclp1Op26ifaBRoGfQ3frCsWCFDgYMG',
            'Content-Type': 'application/json'
        }  

    auth_stagging = "Dh2vxj1C4Mclp1Op26ifaBRoGfQ3frCsWCFDgYMG"

    payload = json.dumps({
        "deliveryType": req.deliveryType,
        "discount_code": "000",
        "packageSize": {
            "type": req.type,
            "depth": req.depth,
            "width": req.width,
            "height": req.height,
            "weight": req.weight,
            "description": req.description,
            "claveProdServ": req.claveProdServ,
            "descripcion_producto": req.description,
            "clave_unidad": "KGM",
            "nombre_unidad": "kilogramo",
            "valor_mercancia": req.value
        },
        "origin": {
            "company_origin": "Traelo origen",
            "street_origin": req.street_origin,
            "interior_number_origin": req.interior_number_origin,
            "outdoor_number_origin": req.outdoor_number_origin,
            "zip_code_origin": req.zip_code_origin,
            "neighborhood_origin": req.neighborhood_origin,
            "city_origin": req.city_origin,
            "state_origin": req.state_origin,
            "references_origin": req.references_origin,
            "name_origin": req.name_origin,
            "email_origin": req.email_origin,
            "phone_origin": req.phone_origin,
            "rfc_origin": req.rfc_origin,
            "save_origin": "false"
        },
        "destination": {
            "company_dest": "Traelo destino",
            "street_dest": req.street_dest,
            "interior_number_dest": req.interior_number_dest,
            "outdoor_number_dest": req.outdoor_number_dest,
            "zip_code_dest": req.zip_code_dest,
            "neighborhood_dest": req.neighborhood_dest,
            "city_dest": req.city_dest,
            "state_dest": req.state_dest,
            "references_dest": req.references_dest,
            "name_dest": req.name_dest,
            "email_dest": req.email_dest,
            "phone_dest": req.phone_dest,
            "save_dest": "false",
            "rfc_dest": req.rfc_dest,
            "ocurre": "false"
        }
        })
    
    # print(request)

    print(headers)
    print(url_orders)
    print(payload)
    response = requests.request("POST", url_orders, headers=headers, data=payload)
    print(response)
    print(response.request)
    print(response.json)
   
    data2 = response.text
    
    # print(data2)
    
   
    respuesta2 = json.loads(data2)
    # print(json_data)
    # print(respuesta2)

    referencia = respuesta2['message']['reason']['reference']
    print(referencia)


    # Etiqueta
    payload_guide = json.dumps({
        "reference": referencia
        })


    response_guide = requests.request("GET", url_mock_guide_pruebas, headers=headers, data=payload_guide)
    # print(response_guide.text)

    etiqueta=''

    if response_guide.status_code == 200 :
        data_guide = response_guide.text
        respuesta2_guide = json.loads(data_guide)
        etiqueta = respuesta2_guide[0]['pdf']
   
    
    print(etiqueta)   

   
    # print(etiqueta)

    # Seguimiento

    #urlsegui_Estafeta = "https://cs.estafeta.com/es/Tracking/searchByGet?wayBill=[NUMERO-DE-GUIA]&wayBillType=0&isShipmentDetail=False"
    #urlsegui_jt = "https://www.jtexpress.mx/trajectoryQuery?waybillNo=guía&flag=1"
    #urlsegui_Redpack = "https://www.redpack.com.mx/es/rastreo/?guias=guía"
    #urlsegui_PaqueteExpress = "https://www.paquetexpress.com.mx/rastreo/guía"

    if (req.deliveryType == "ESTAFETA_EXPRESS" or req.deliveryType == "ESTAFETA_ECONOMICO"):
            urlsegui = "https://cs.estafeta.com/es/Tracking/searchByGet?wayBill="+referencia+"&wayBillType=0&isShipmentDetail=False"
    elif (req.deliveryType == "EXPRESS" or req.deliveryType == "ECOEXPRESS" or req.deliveryType == "METROPOLITANO"):
         urlsegui = "https://www.redpack.com.mx/es/rastreo/?guias="+referencia        
    elif (req.deliveryType == "STANDARD_JT"):
         urlsegui = "https://www.jtexpress.mx/trajectoryQuery?waybillNo="+referencia+"&flag=1"
    elif (req.deliveryType == "EXPRESS_DOMESTIC" or req.deliveryType == "ECONOMY_SELECT_DOMESTIC"):
        urlsegui = "https://www.dhl.com/mx-es/home/tracking/tracking-ecommerce.html?submit=1&tracking-id="+referencia
    elif (req.deliveryType == "STD-T"):
         urlsegui = "https://www.paquetexpress.com.mx/rastreo/"+referencia+"&flag=1"
    # elif (req.deliveryType == "METROPOLITANO"):
    #     urlsegui = "https://www.paquetexpress.com.mx/rastreo/"+referencia

    # Recogida / pickup

    payload_pickup = json.dumps({
        "date": req.fecha_recogida,
        "time": req.hora_recogida_desde,
        "reference": referencia
        })
    
    print(payload_pickup)
    response_pickup = requests.request("POST", url_mock_pickup_pruebas, headers=headers, data=payload_pickup)
    print(response_pickup.status_code)
    

    # respuesta final

    if  response_pickup.status_code == 200:
        data_pickup = response_pickup.text
        respuesta2_pickup = json.loads(data_pickup)
        print(respuesta2_pickup)
        recogida_estado = respuesta2_pickup['message']['PickupConfirmationNumber']
        print(recogida_estado)
        response3 = {'resultado': "1","numero_rastreo": referencia, "url_rastreo":urlsegui, "etiqueta": etiqueta, "codigo_recogida": recogida_estado}
    else:
        response3 = {'resultado': "0","numero_rastreo": referencia, "url_rastreo":urlsegui, "etiqueta": etiqueta, "codigo_recogida": '0'}

    print(response3)

    #prueba = recogida_estado
    return response3

