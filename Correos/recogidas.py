from pydantic import BaseModel
from typing import Optional
from typing import List

class Recogidas_Details(BaseModel):
    referenciaRecogida: Optional[str] = None
    fecRecogida: str 
    horaRecogida: str
    codAnexo: str
    nomNombreViaRec: str
    nomLocalidadRec: str
    codigoPostalRecogida: str
    desPersonaContactoRec: Optional[str] = None
    desTelefContactoRec: Optional[str] = None
    desEmailContactoRec: Optional[str] = None
    desObservacionRec: Optional[str] = None
    numEnvios: int
    numPeso: int
    tipoPesoVol: int
    indImprimirEtiquetas: str
    indDevolverCodSolicitud: str
    listaCodEnvios: List[str]

""" Details Structure
ReferenciaRecogida: ReferenciaRecogida: Client reference. It could be the same as ReferenciaRelacionPaP.
FecRecogida: FecRecogida: Pick up date. Format: “dd/MM/yyyy”. If format is not correct or is less than the current
date, an error is returned.
HoraRecogida: HoraRecogida: Pick up time. Format: “HH:mm”. If format is not correct, an error is returned.
CodAnexo: CodAnexo: Client Annex. If empty, an error returned.
NomNombreViaRec: NomNombreViaRec: Pick up street name. If empty, an error returned.
NomLocalidadRec: NomLocalidadRec: Pick up city. If empty, an error returned.
CodigoPostalRecogida: CodigoPostalRecogida: Pick up postal code. If empty, an error returned.
DesPersonaContactoRec: DesPersonaContactoRec: (Optional) Pick up contact person.
DesTelefContactoRec: DesTelefContactoRec: (Optional) Pick up contact phone number.
DesEmailContactoRec: DesEmailContactoRec: (Optional) Pick up contact email.
DesObservacionRec: DesObservacionRec: (Optional) Pick up observations.
NumEnvios: NumEnvios: Parcel number to pick up. If empty, an error returned.
NumPeso: NumPeso: Estimated weight value, in grams. If empty, an error returned.
TipoPesoVol: Volumetric weight. Possible value:
• 10 Envelopes
• 20 Small (shoe box)
• 30 Medium (box packages folios)
• 40 Large (box 80x80x80 cm)
• 50 Very large (larger than 80x80x80 cm box)
• 60 Palet
IndImprimirEtiquetas: IndImprimirEtiquetas: Indicates if label printing is required. Possible value “S”, “N”.
IndDevolverCodSolicitud: Indicates if pick up code is returned. “S” – Returns pick up code.
ListaCodEnvios: Shipment code list.
CodigoEnvio: Shipment code. Mandatory if IndImprimirEtiquetas = “S”. 
"""

class Recogidas_Request(BaseModel):
    prod: int
    referenciaRelacionPaP: str
    tipoOperacion: str
    fechaOperacion: str
    numContrato: int
    numDetallable: int
    CodSistema: Optional[str] = None
    codUsuario: str
    recogidasDetalles: Recogidas_Details

""" Request Structure
ReferenciaRelacionPaP: Client reference. It does not have to be unique, it is possible repetition.
TipoOperacion: Operation to perform. Possible values: "ALTA".
FechaOperacion: FechaOperacion: Date of operation. Format: “dd-MM-yyyy HH:mm:ss”. If format is not correct or is less
than the current date an error is returned.
NumContrato: NumContrato: Contract number. If empty, an error returned.
NumDetallable: NumDetallable: Client (detallable) number. If empty, an error returned.
CodSistema: CodSistema: (Optional) Calling system code.
CodUsuario: OV2 user. If empty, an error returned. e.g.: pedroperez19 
"""

class Recodigas_Response(BaseModel):
    codigoError: int
    descripcionError: str
    codSolicitud: str

""" Response XML Message
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
    <soapenv:Body>
        <ns3:SolicitudRegistroRecogidaResult xmlns:ns3="http://www.correos.es/ServicioPuertaAPuertaBackOffice" xmlns:ns2="http://www.correos.es/ServicioPuertaAPuerta">
            <ns3:RespuestaSolicitudRegistroRecogida>
                <CodigoError><!-- Valores:“1”:KO”, Vacio:OK --></CodigoError>
                <DescripcionError><!—Descripción error--></DescripcionError>
                <CodSolicitud><!-- Código solicitud --></CodSolicitud>
            </ns3:RespuestaSolicitudRegistroRecogida>
        </ns3:SolicitudRegistroRecogidaResult>
    </soapenv:Body>
</soapenv:Envelope>
"""

""" Request XML Message
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="http://www.correos.es/ServicioPuertaAPuertaBackOffice" xmlns:ser1="http://www.correos.es/ServicioPuertaAPuerta">
    <soapenv:Header/>
    <soapenv:Body>
        <ser:SolicitudRegistroRecogida>
            <ReferenciaRelacionPaP>1245190d-c594-4e8484nc890</ReferenciaRelacionPaP>
            <TipoOperacion><!— Operación --></TipoOperacion>
            <FechaOperacion><!— Fecha de la operación --></FechaOperacion>
            <NumContrato>><!— Contrato --></NumContrato>
            <NumDetallable><!— Detallable --></NumDetallable>
            <CodSistema><!— Código de Sistema de Correos --></CodSistema>
            <CodUsuario><!— Identificador del usuario OV2 --></CodUsuario>
            <ser1:Recogida>
                <ReferenciaRecogida><!— Referencia --></ReferenciaRecogida>
                <FecRecogida><!— Fecha de la recogida --></FecRecogida>
                <HoraRecogida><!— Hora de la recogida --></HoraRecogida>
                <CodAnexo><!— Anexo --></CodAnexo>
                <NomNombreViaRec><!— Calle o vía --></NomNombreViaRec>
                <NomLocalidadRec><!— Localidad --></NomLocalidadRec>
                <CodigoPostalRecogida><!— Código Postal --></CodigoPostalRecogida>
                <DesPersonaContactoRec><!— Persona de contacto --></DesPersonaContactoRec>
                <DesTelefContactoRec><!— Teléfono --></DesTelefContactoRec>
                <DesEmailContactoRec><!— email --></DesEmailContactoRec>
                <DesObservacionRec><!— Observaciones --></DesObservacionRec>
                <NumEnvios><!— Cantidad de envíos --></NumEnvios>
                <NumPeso><!— Peso estimado --></NumPeso>
                <TipoPesoVol><!— Código del peso volumétrico estimado --></TipoPesoVol>
                <IndImprimirEtiquetas><!— Impresión de etiquetas --></IndImprimirEtiquetas>
                <IndDevolverCodSolicitud><!— Solicitar código solicitud generada --></IndDevolverCodSolicitud>
                <ser1:ListaCodEnvios>
                    <CodigoEnvio><!— Código envío a recoger--></CodigoEnvio>
                </ser1:ListaCodEnvios>
            </ser1:Recogida>
        </ser:SolicitudRegistroRecogida>
    </soapenv:Body>
</soapenv:Envelope>
"""

