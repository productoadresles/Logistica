




##############

import requests
import urllib3
#from urllib2 import urlopen
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

class ReqShipmentCreate(BaseModel):
    id_usuario: Optional[str] = None

class ReqStatus(BaseModel):
    codigo_envio: str

app = FastAPI()

handler = Mangum(app)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Llamadas GLS 

@app.post("/shipment_create_envios_perros")
async def shipment_create_envios_perros(req: ReqShipmentCreate):
    
    url_pruebas = "https://staging-app.enviosperros.com/api/v2/orders"
    url_product = "https://app.enviosperros.com/api/v2/orders"

    auth_stagging = "Bearer TAZ56gshihIMTjLrSZly1vZGXe1e1JIDRs39IpNCOA9l5vby3llfYaQxpTS8"

    http = urllib3.PoolManager()

    payload = """
    {
        "deliveryType": "ESTAFETA_EXPRESS",
        "packageSize": {
        "type": "Caja",
        "depth": "5",
        "width": "5",
        "height": "5",
        "weight": "1",
        "description": "papeles",
        "claveProdServ": "01010101",
        "descripcion_producto": "papas",
        "clave_unidad": "KGM",
        "nombre_unidad": "kilogramo",
        "valor_mercancia": "150.28"
        },
        "origin": {
        "company_origin": "Eviosperros",
        "street_origin": "5 de mayo",
        "interior_number_origin": "",
        "outdoor_number_origin": "69",
        "zip_code_origin": "91726",
        "neighborhood_origin": "independencia",
        "city_origin": "Boca del río",
        "state_origin": "Veracruz de Ignacio de la Llave",
        "references_origin": "porton blanco",
        "name_origin": "Ana maria",
        "email_origin": "ejemplo@gmail.com",
        "phone_origin": "2291234567",
        "rfc_origin": "AAA010101AAA",
        "save_origin": "false"
        },
        "destination": {
        "company_dest": "Test company",
        "street_dest": "5 de mayo",
        "interior_number_dest": "",
        "outdoor_number_dest": "69",
        "zip_code_dest": "91726",
        "neighborhood_dest": "independencia",
        "city_dest": "Boca del río",
        "state_dest": "Veracruz de Ignacio de la Llave",
        "references_dest": "puerta negra",
        "name_dest": "Eduardo Gonzalez",
        "email_dest": "ejemplo@gmail.com",
        "phone_dest": "2291234569",
        "save_dest": "false",
        "rfc_dest": "XAXX010101000",
        "ocurre": "false"
        }
    }
    """

    payload_2 = {"deliveryType": "ESTAFETA_EXPRESS", "packageSize": {"type": "Caja", "depth": "5", "width": "5", "height": "5", "weight": "1", "description": "papeles", "claveProdServ": "01010101", "descripcion_producto": "papas", "clave_unidad": "KGM", "nombre_unidad": "kilogramo", "valor_mercancia": "150.28"}, "origin": {"company_origin": "Eviosperros", "street_origin": "5 de mayo", "interior_number_origin": "", "outdoor_number_origin": "69", "zip_code_origin": "91726", "neighborhood_origin": "independencia", "city_origin": "Boca del río", "state_origin": "Veracruz de Ignacio de la Llave", "references_origin": "porton blanco", "name_origin": "Ana maria", "email_origin": "ejemplo@gmail.com", "phone_origin": "2291234567", "rfc_origin": "AAA010101AAA", "save_origin": "false"}, "destination": {"company_dest": "Test company", "street_dest": "5 de mayo", "interior_number_dest": "", "outdoor_number_dest": "69", "zip_code_dest": "91726", "neighborhood_dest": "independencia", "city_dest": "Boca del río", "state_dest": "Veracruz de Ignacio de la Llave", "references_dest": "puerta negra", "name_dest": "Eduardo Gonzalez", "email_dest": "ejemplo@gmail.com", "phone_dest": "2291234569", "save_dest": "false", "rfc_dest": "XAXX010101000", "ocurre": "false"}}

    headers = {
        "Content-Type": "application/json",
        "Authentication": "Bearer 7D2tCjtpoc4STBh14cCPjcRphKyKtCGLE9umYwxH"
    }

    headers2 = {
        'Authentication': 'Bearer 7D2tCjtpoc4STBh14cCPjcRphKyKtCGLE9umYwxH',
        'Content-Type': 'application/json',
        'Cookie': 'XSRF-TOKEN=eyJpdiI6IkZIREJIc205UU05SUt1Y09xQVlYbFE9PSIsInZhbHVlIjoiQ1FpKzFjNzlqVHdkZHdSNnNzTlIyTnpVMlB4RHBMSkhzYWoybUZIaVVDdTRZTWVGeTJOWWYyUDFqZStFaExjT0ZwNXZ4bUxQV2pCR3VvSDVZVkQybnNtdEkxV2ZHN3B2VVUxVkRUcVZ1K2JtZjBvL3BobjZPVWNGYnJxRW5rT1QiLCJtYWMiOiIwYjA4OWE4OGUyOGFiYjkzNjY2YjBjODQ2MzgxYmZhYzYxMzdmMDk0YTE5ODMyYzk2NDUwMDM0MjQwN2E2ZmIwIiwidGFnIjoiIn0%3D; enviosperros_session=eyJpdiI6InV4eDhjcmtzekIxS2tDcmt1WGZIQnc9PSIsInZhbHVlIjoiYlhoeURkdVpKdUNqUFcvc1lpUDZuVmFiTTEyaUZPZmVvcHVFeHIxekpqM08wV2ZxbzUzUXZPRjdTZDdMZFdoYW1IQVNuQnlRaDh2Z2E3R0RWanpGQ1pKVk9YNWZSUlhPdnBhY29rbC9RZ2FSUmd1YWdQZmVUc3N4MmxmWGVpNkUiLCJtYWMiOiIwNWNhMDcwZjBkOGE3ZmNiZTdmODMxZjMzYzE4OTQxMzg1N2E3ODA4ODQ1ZTM0MzZlMzQ1OWVjYjQ5OTdhNDIzIiwidGFnIjoiIn0%3D'
    }


    #response = requests.request("POST", url_pruebas, data=payload_2, headers=headers2)
    #response_body = urlopen(request).read()
    url = url_pruebas + payload

    response2 = http.request(
        "POST",
        url_pruebas,
        body=payload,
        headers=headers2
    )
    
    respue = response2.data.decode('utf-8')

    #print(response2.text)
    #response = requests.post(url_pruebas, headers=headers2, data=payload)
    #respue = (response2.text)
    #contesta_dict = xmltodict.parse(respue)


    #response_body = urlopen(response).read()

    #return response2
    return respue


################



    http = urllib3.PoolManager()

    #request = request(url_pruebas, data=values, headers=headers)
    #req = requests.request("POST", url_pruebas, data=values, headers=headers)
    req = http.request(
        "POST",
        url_pruebas,
        body=values,
        headers=headers
    )

    #response_body = urlopen(response).read()
    #response_2 = (response.text)