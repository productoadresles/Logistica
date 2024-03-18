from typing import Optional
from typing import List
from fastapi import FastAPI, Path
from pydantic import BaseModel
from mangum import Mangum
import random
import base64

import requests

import json
import xml.dom.minidom
import xmltodict

#Pre register shipment vars
from vars import PR_PRE_URL, PR_URL, PREREGISTER_AUTH, PREREGISTER_PRE_AUTH
from preregistro import PreRegister_Response, PreRegister_Response_File, PreRegister_Response_Package, Shipment

#Pickup vars
from vars import PICKUP_PRE_URL, PICKUP_URL, PICKUP_AUTH, PICKUP_PRE_AUTH
from recogidas import Recogidas_Request, Recodigas_Response

#Tracking vars
from vars import TRACK_PRE_URL, TRACK_URL, TRACK_AUTH, TRACK_PRE_AUTH
from seguimiento import Tracking_Response


import xml.etree.ElementTree as ET
from datetime import datetime

null = 'null'
false = False

class back(BaseModel):
    servicio: str
    id_usuario: str

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
    

@app.post("/PreRegister",
          description="Pre register a package and address for shipping with Correos")
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
    print('Response: ',response)
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

@app.post("/Pickup",
          description="Setup a pickup from correos for a previously registered shipment")
async def pickup_correos (req: Recogidas_Request):
    #print(req)
    #print(req.recogidasDetalles)

    if req.prod == 0:
        auth = PICKUP_PRE_AUTH
        url = PICKUP_PRE_URL
        req.numContrato = 99999999
        req.numDetallable = 99999999
        req.recogidasDetalles.codAnexo = "091"
    else:
        auth = PICKUP_AUTH
        url = PICKUP_URL

    # Cabeceras
    headers = {
        'Content-Type': 'text/xml; charset=UTF-8'
    }

    payload = f"""
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="http://www.correos.es/ServicioPuertaAPuertaBackOffice" xmlns:ser1="http://www.correos.es/ServicioPuertaAPuerta">
    <soapenv:Header/>
    <soapenv:Body>
        <ser:SolicitudRegistroRecogida>
            <ReferenciaRelacionPaP>{req.referenciaRelacionPaP}</ReferenciaRelacionPaP>
            <TipoOperacion>>{req.tipoOperacion}</TipoOperacion>
            <FechaOperacion>>{req.fechaOperacion}</FechaOperacion>
            <NumContrato>>>{req.numContrato}</NumContrato>
            <NumDetallable>>{req.numDetallable}</NumDetallable>
            <CodSistema>>{req.CodSistema}</CodSistema>
            <CodUsuario>>{req.codUsuario}</CodUsuario>
            <ser1:Recogida>
                <ReferenciaRecogida>{req.recogidasDetalles.referenciaRecogida if req.recogidasDetalles.referenciaRecogida != "" else req.referenciaRelacionPaP}</ReferenciaRecogida>
                <FecRecogida>{req.recogidasDetalles.fecRecogida}</FecRecogida>
                <HoraRecogida>{req.recogidasDetalles.horaRecogida}</HoraRecogida>
                <CodAnexo>{req.recogidasDetalles.codAnexo}</CodAnexo>
                <NomNombreViaRec>{req.recogidasDetalles.nomNombreViaRec}</NomNombreViaRec>
                <NomLocalidadRec>{req.recogidasDetalles.nomLocalidadRec}</NomLocalidadRec>
                <CodigoPostalRecogida>{req.recogidasDetalles.codigoPostalRecogida}</CodigoPostalRecogida>
                <DesPersonaContactoRec>{req.recogidasDetalles.desPersonaContactoRec}</DesPersonaContactoRec>
                <DesTelefContactoRec>{req.recogidasDetalles.desTelefContactoRec}</DesTelefContactoRec>
                <DesEmailContactoRec>{req.recogidasDetalles.desEmailContactoRec}</DesEmailContactoRec>
                <DesObservacionRec>{req.recogidasDetalles.desObservacionRec}</DesObservacionRec>
                <NumEnvios>{req.recogidasDetalles.numEnvios}</NumEnvios>
                <NumPeso>{req.recogidasDetalles.numPeso}</NumPeso>
                <TipoPesoVol>{req.recogidasDetalles.tipoPesoVol}</TipoPesoVol>
                <IndImprimirEtiquetas>{req.recogidasDetalles.indImprimirEtiquetas}</IndImprimirEtiquetas>
                <IndDevolverCodSolicitud>{req.recogidasDetalles.indDevolverCodSolicitud}</IndDevolverCodSolicitud>
                <ser1:ListaCodEnvios>"""
    
    for i in req.recogidasDetalles.listaCodEnvios:
                    payload += f"""
                    <CodigoEnvio>{i}</CodigoEnvio>
                    """
    
    payload += f"""
                </ser1:ListaCodEnvios>
            </ser1:Recogida>
        </ser:SolicitudRegistroRecogida>
    </soapenv:Body>
</soapenv:Envelope>
"""

    response = requests.post(url=url, auth=auth, headers=headers, data=payload)
    response_body = xmltodict.parse(response.text)['soapenv:Envelope']['soapenv:Body']['SolicitudRegistroRecogidaResult']['RespuestaSolicitudRegistroRecogida']

    devuelve = Recodigas_Response(codigoError=response_body['CodigoError'],
                                  descripcionError=response_body['DescripcionError'],
                                  codSolicitud=response_body['CodSolicitud'])
    return devuelve

@app.get("/Tracking/{prod}&shipments={shipments}",
         description="Get tracking status from the shipment")
async def tracking_correos (prod: int = Path(..., description="Specify to request from PROD or PRE PROD"),
                            shipments: str = Path(..., description="List of shipment codes to trace"),
                            languageCode: Optional[str] = "ES",
                            showTraceHistory: Optional[int] = 1): #Path(1, description="0 - Show only last trace, 1 - Show all trace history")):

    if prod == 0:
        user, password = TRACK_PRE_AUTH 
        url = TRACK_PRE_URL
    else:
        user, password = TRACK_AUTH  
        url = TRACK_URL

    params={'envios': shipments,
            'codIdioma': languageCode,
            'indUltEvento': "N" if showTraceHistory == 1 else "S"}
    encoded_ath = base64.b64encode(str(user+":"+password).encode("utf-8")).decode()
    # print(f"str(user+':'+password).encode('base64') = str({user}:{password}).encode('base64') = {encoded_ath}")
    headers = {
        "Authorization": f"Basic {encoded_ath}",
        "Content-Type": "application/json"}
        #"": shipments}
    # print(f'headers: {headers}')

    # url = "https://localizador.correos.es/canonico/eventos_envio_servicio_auth/"
    url += shipments+"?"+f"&codIdioma={languageCode}"+"&indUltEvento=" + "N" if showTraceHistory == 1 else "S"
    response = {"success": 0}
    try:
        #url = "https://localizador.correos.es/canonico/eventos_envio_servicio_auth/"#PQ43B404AA015110128001N?codIdioma=ES&indUltEvento=N"
        print(url)
        response = requests.get(url, headers=headers)#, params=params)
        print(response.status_code)
    except Exception:
         print("Couldn't successfuly execute this request!")
    print('response',response)
    #response = requests.text

    return response