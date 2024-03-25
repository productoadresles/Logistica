from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum

import requests
import json

null = 'null'
false = False

class ReqAgencies(BaseModel):

    peso: int
    largo: int
    ancho: int
    alto: int
    codigo_recogida: str
    poblacion_recogida: Optional[str] = None
    codigo_pais_recogida: str
    codigo_entrega: str
    poblacion_entrega: Optional[str] = None
    codigo_pais_entrega: str
    codigo_promo: Optional[str] = None

class ReqPickUpTimes(BaseModel):
    codigo_recogida: str
    id_agencia: str
    fecha_recogida: str #fecha en formato "dd/mm/yyyy"

class ReqShipmentCreate(BaseModel):
    prod: str
    peso: int
    largo: int
    ancho: int
    alto: int
    contenido: Optional[str] = None
    taric: Optional[str] = None
    peso_bruto: Optional[str] = None
    peso_neto: Optional[str] = None
    cantidad: Optional[int] = None
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
    recoger_tienda: Optional[str] = None
    cod_promo: Optional[str] = None
    select_oficinas_destino: Optional[str] = None
    fecha_recogida: str
    hora_recogida_desde: str
    hora_recogida_hasta: str
    unidad_correo: Optional[str] = None
    codigo_envio_servicio: Optional[str] = None
    id_agencia: str
    cn: int
    servicio: str
    id_usuario: str

class ReqStatus(BaseModel):
    codigo_envio: str

app = FastAPI()

handler = Mangum(app)

@app.get("/")
async def root():
    return {"message": "API de GENEI"}

@app.post("/list_agencies")
async def agencies_list(request: ReqAgencies):

    if request.codigo_pais_recogida == "ES" or request.codigo_pais_entrega == "ES":
        req = {
        "array_bultos": [
                        [
                        
                        ],
                        {
                        "peso": str(request.peso),
                        "largo": str(request.largo),
                        "ancho": str(request.ancho),
                        "alto": str(request.alto)}
                        ],
        "codigos_origen": request.codigo_recogida,
        "poblacion_salida": request.poblacion_recogida,
        "iso_pais_salida": request.codigo_pais_recogida,
        "codigos_destino": request.codigo_entrega,
        "poblacion_llegada": request.poblacion_entrega,
        "iso_pais_llegada": request.codigo_pais_entrega,
        "cod_promo": request.codigo_promo,
        "usuario_servicio": "soporte@adresles.com86",
        "password_servicio": "ls9regxc",
        "servicio": "api"
        }

        URL = 'https://www.genei.es/json_interface/obtener_listado_agencias_precios'

        res = requests.post( url = URL, json = req)

        responsejson = res.json()

        if responsejson['datos_agencia2']:
            response = {'agencias': list(responsejson['datos_agencia2'].values())}
        else:
            response = {'agencias': list()}
    else:
        response = {'agencias': list()}

    return response


@app.post("/pickup_times")
async def pickup_times(request: ReqPickUpTimes):

    req = {
    "cp_salida":request.codigo_recogida,
    "id_agencia":request.id_agencia,
    "fecha_recogida":request.fecha_recogida,
    "usuario_servicio": "soporte@adresles.com86",
    "password_servicio": "ls9regxc",
    "servicio":"api"
    }

    URL = 'https://www.genei.es/json_interface/obtener_lista_horarios_disponibles_agencia'

    res = requests.post( url = URL, json = req)

    responsejson = res.json()
    
    if responsejson == false:
        response = {'inicial': list(), 
                    'final': list()}
    else:
        response = {'inicial': list(responsejson['inicial'].values()), 
                    'final': list(responsejson['final'].values())}

    return response


@app.post("/shipment_create")
async def shipment_create(req: ReqShipmentCreate):

    request = {
    "array_bultos": [
                     [], {
                          "peso": str(req.peso),
                          "largo": str(req.largo),
                          "ancho": str(req.ancho),
                          "alto": str(req.alto),
                          "contenido": req.contenido,
                          "taric": req.taric,
                          "peso_bruto": req.peso_bruto,
                          "peso_neto": req.peso_neto,
                          "cantidad": str(req.cantidad),
                          "valor": req.valor
                          }
                     ],
        "stock": [
        ],
        "valor_mercancia": req.valor_mercancia,
        "contenido_envio": req.contenido_envio,
        "contrareembolso": req.contrareembolso,
        "cantidad_reembolso": req.cantidad_reembolso,
        "seguro": req.seguro,
        "dia_laborable_automatico": req.dia_laborable_automatico,
        "importe_seguro": req.importe_seguro,
        "dropshipping": req.dropshipping,
        "codigos_origen": req.codigos_origen,
        "poblacion_salida": req.poblacion_salida,
        "iso_pais_salida": req.iso_pais_salida,
        "direccion_salida": req.direccion_salida,
        "email_salida": req.email_salida,
        "nombre_salida": req.nombre_salida,
        "telefono_salida": req.telefono_salida,
        "codigos_destino": req.codigos_destino,
        "poblacion_llegada": req.poblacion_llegada,
        "iso_pais_llegada": req.iso_pais_llegada,
        "direccion_llegada": req.direccion_llegada,
        "telefono_llegada": req.telefono_llegada,
        "email_llegada": req.email_llegada,
        "nombre_llegada": req.nombre_llegada,
        "dni_llegada": req.dni_llegada,
        "observaciones_salida": req.observaciones_salida,
        "contacto_salida": req.contacto_salida,
        "observaciones_llegada": req.observaciones_llegada,
        "contacto_llegada": req.contacto_llegada,
        "codigo_mercancia": req.codigo_mercancia,
        "recoger_tienda": req.recoger_tienda,
        "cod_promo": req.cod_promo,
        "select_oficinas_destino": req.select_oficinas_destino,
        "fecha_recogida": req.fecha_recogida,
        "hora_recogida_desde": req.hora_recogida_desde,
        "hora_recogida_hasta": req.hora_recogida_hasta,
        "unidad_correo": req.unidad_correo,
        "codigo_envio_servicio": req.codigo_envio_servicio,
        "id_agencia": req.id_agencia,
        "usuario_servicio": "soporte@adresles.com86",
        "password_servicio": "ls9regxc",
        "cn": req.cn,
        "servicio": req.servicio,
        "id_usuario": req.id_usuario
    }

    if req.prod == "1":
        URL = 'https://www.genei.es/json_interface/crear_envio'
    else:
        URL = 'https://www.genei.es/json_interface/crear_envio_sandbox'

    res = requests.post( url = URL, json = request)
    
    print(res)

    # responsejson = res.json()

    # if responsejson['resultado'] == "1":
    #     response = {'resultado': "1",
    #                 "codigo_envio": responsejson['codigo_envio']
    #             }

    # else:
    #     response = {'resultado': "0",
    #                 "codigo_envio": ""
    #                 }

    return ''

@app.post("/status")
async def pickup_times(request: ReqStatus):

    req = {
    "codigo_envio_plataforma":request.codigo_envio,
    "usuario_servicio": "soporte@adresles.com86",
    "password_servicio": "ls9regxc",
    "servicio":"api"
    }

    URL = 'https://www.genei.es/json_interface/obtener_codigo_envio'

    res = requests.post( url = URL, json = req)

    responsejson = res.json()

    response = responsejson

    return response