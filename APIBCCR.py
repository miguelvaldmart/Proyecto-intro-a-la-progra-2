import requests
from datetime import datetime
import xml.etree.ElementTree as ET

class TipoCambioBCCR:
    def __init__(self, correo: str, token: str):
        self.correo = correo
        self.token = token
        self.url = (
            "https://gee.bccr.fi.cr/Indicadores/Suscripciones/WS/wsindicadoreseconomicos.asmx/"
            "ObtenerIndicadoresEconomicos" # URL del servicio web del BCCR. Está en la documentación oficial del BCCR
        )

    def obtener_tipo_cambio(self, indicador: str, fecha: datetime = None) -> float:
        if fecha is None:
            fecha = datetime.now()

        fecha_str = fecha.strftime("%d/%m/%Y")

        params = {
            "Indicador": indicador,
            "FechaInicio": fecha_str,
            "FechaFinal": fecha_str,
            "Nombre": "consulta-api",
            "SubNiveles": "N",
            "CorreoElectronico": self.correo,
            "Token": self.token
        }

        response = requests.get(self.url, params=params)
        response.raise_for_status()

        root = ET.fromstring(response.text)
        valor = root.find('.//NUM_VALOR')
        return float(valor.text) if valor is not None else None

    def obtener_compra(self) -> float:
        return self.obtener_tipo_cambio("317") # el indicador "317" es el tipo de cambio de compra

    def obtener_venta(self) -> float:
        return self.obtener_tipo_cambio("318") # el indicador "318" es el tipo de cambio de venta


# Uso de la clase
if __name__ == "__main__":
    correo = "cuentacoc1er@gmail.com"  # Reemplazar con su correo electrónico
    token = "AAAOLNP5CM"  # Reemplazar con su token de acceso

    bccr = TipoCambioBCCR(correo, token) #Aquí se crea una instancia de la clase con el correo y token

    try: # El try es por si hay un error al consultar el servicio
        compra = bccr.obtener_compra()
        venta = bccr.obtener_venta()

        print(f"Tipo de cambio de compra: {compra}")
        print(f"Tipo de cambio de venta: {venta}")
    except requests.RequestException as e: # si hay un error al hacer la petición cae aquí
        print(f"Error al consultar el servicio del BCCR: {e}")