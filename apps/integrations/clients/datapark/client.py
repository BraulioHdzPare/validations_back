"""Cliente SOAP (zeep) para la interfaz Web Validations de Datapark (DpWebService).

- Binding BasicHttpBinding (SOAP 1.1), autenticación HTTP Basic.
- El WSDL publica dos puertos (uno HTTP alcanzable y uno HTTPS interno que no lo
  es); fijamos explícitamente el binding al endpoint configurado.
"""
import logging

from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client, Settings
from zeep.transports import Transport

logger = logging.getLogger(__name__)

# QName del binding HTTP del servicio (ns1 = http://tempuri.org/).
BINDING_QNAME = "{http://tempuri.org/}BasicHttpBinding_IValidationService"

# Constantes de Datapark.
MEDIA_TYPE_BARCODE = 2
USAGE_TYPE_TRANSIENT = 2


class DataparkClient:
    """Envoltorio delgado sobre el DpWebService de Datapark."""

    def __init__(self, *, base_url, username="", password="", timeout=20):
        self.base_url = base_url

        session = Session()
        if username:
            session.auth = HTTPBasicAuth(username, password) # Autenticación HTTP Basic para el endpoint SOAP
        session.verify = False  # endpoint HTTP / certificado interno

        transport = Transport(session=session, timeout=timeout) # Transporta las solicitudes SOAP usando la sesión configurada
        settings = Settings(strict=False, xml_huge_tree=True) # Configuración de Zeep para manejar XML grandes y no estrictos

        self._client = Client(wsdl=self._wsdl_url(base_url), transport=transport, settings=settings) # Crea un cliente Zeep para el WSDL del servicio, usando el transporte y la configuración definidos
        # Operaciones fijadas al endpoint configurado (no al puerto HTTPS interno).
        self._service = self._client.create_service(BINDING_QNAME, base_url)

    @staticmethod
    def _wsdl_url(base_url: str) -> str:
        return base_url if "?" in base_url else base_url + "?wsdl"

    @classmethod
    def from_config(cls, config):
        """Construye el cliente desde un IntegrationConfig (password se descifra solo)."""
        return cls(
            base_url=config.base_url,
            username=config.username,
            password=config.encrypted_password,
            timeout=config.timeout_seconds or 20,
        )

    # -- Operaciones sin parámetros (diagnóstico / catálogo) -----------------

    def get_service_version(self) -> str:
        return self._service.GetServiceVersion()

    def get_merchants(self):
        return self._service.GetMerchants()

    def get_discounts(self):
        return self._service.GetDiscounts()

    def get_discounts_for_merchant(self, merchant_id: int):
        return self._service.GetDiscountsForMerchant(merchant_id)

    def get_max_validations_count(self) -> int:
        return self._service.GetMaxValidationsCount()

    # -- Consulta de boleto --------------------------------------------------

    def query_card_entry(
        self,
        *,
        card_number: str,
        media_type: int = MEDIA_TYPE_BARCODE,
        usage_type: int = USAGE_TYPE_TRANSIENT,
        discount_key: int = 0,
        calculate_amount: bool = False,
    ):
        return self._service.QueryCardEntry(
            obQCData={
                "CardNumber": card_number,
                "CardMediaType": media_type,
                "CardUsageType": usage_type,
                "DiscountKey": discount_key,
                "HaveToCalculateAmountDue": calculate_amount,
            }
        )
