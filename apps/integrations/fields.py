"""Cifrado transparente de campos sensibles (credenciales de integraciones).

Usa Fernet (cryptography). La llave se toma de ``settings.FIELD_ENCRYPTION_KEY``,
que a su vez se lee de la variable de entorno ``FIELD_ENCRYPTION_KEY`` (.env).

Comportamiento:
- Con llave configurada: cifra al guardar, descifra al leer. Es tolerante a
  valores legados en texto plano (no revienta; los devuelve tal cual hasta que
  se vuelvan a guardar y queden cifrados).
- Sin llave configurada: el campo se comporta como un ``TextField`` normal
  (cifrado deshabilitado). Útil durante la transición o en entornos sin llave.
"""
import logging

from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
from django.db import models

logger = logging.getLogger(__name__)

_warned_no_key = False


def _get_fernet():
    """Devuelve un Fernet con la llave de settings, o None si no hay llave."""
    global _warned_no_key
    key = getattr(settings, "FIELD_ENCRYPTION_KEY", "") or ""
    if not key:
        if not _warned_no_key:
            logger.warning(
                "FIELD_ENCRYPTION_KEY no está configurada: los campos cifrados se "
                "guardarán en texto plano hasta que definas la llave en .env."
            )
            _warned_no_key = True
        return None
    if isinstance(key, str):
        key = key.encode()
    return Fernet(key)


def encrypt(value: str) -> str:
    fernet = _get_fernet()
    if fernet is None:
        return value
    return fernet.encrypt(value.encode()).decode()


def decrypt(value: str) -> str:
    fernet = _get_fernet()
    if fernet is None:
        return value
    try:
        return fernet.decrypt(value.encode()).decode()
    except InvalidToken:
        # Valor legado en texto plano (no cifrado con esta llave). Tolerar.
        return value


class EncryptedTextField(models.TextField):
    """TextField que cifra/descifra su contenido de forma transparente.

    En la BDD se guarda el ciphertext; en Python el atributo entrega el texto
    plano. Nota: por diseño no se puede filtrar (`.filter(...)`) por estos
    campos, ya que el cifrado no es determinista.
    """

    description = "TextField con cifrado transparente (Fernet)"

    def from_db_value(self, value, expression, connection):
        if value is None or value == "":
            return value
        return decrypt(value)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is None or value == "":
            return value
        return encrypt(value)
