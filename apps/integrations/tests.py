from cryptography.fernet import Fernet
from django.db import connection
from django.test import TestCase, override_settings

from apps.integrations.fields import decrypt, encrypt
from apps.integrations.models import IntegrationConfig

TEST_KEY = Fernet.generate_key().decode()


@override_settings(FIELD_ENCRYPTION_KEY=TEST_KEY)
class EncryptedFieldTests(TestCase):
    """Cifrado activo (con llave Fernet de prueba)."""

    def test_encrypt_decrypt_roundtrip(self):
        token = encrypt("secreto-123")
        self.assertNotEqual(token, "secreto-123")        # se cifró
        self.assertEqual(decrypt(token), "secreto-123")  # round-trip

    def test_db_stores_ciphertext_but_orm_returns_plaintext(self):
        cfg = IntegrationConfig.objects.create(
            name="Test DP",
            system_type="DATAPARK",
            encrypted_password="miSecreto",
        )

        # El ORM entrega texto plano.
        reloaded = IntegrationConfig.objects.get(pk=cfg.pk)
        self.assertEqual(reloaded.encrypted_password, "miSecreto")

        # La columna cruda en la BDD guarda ciphertext (no el texto plano).
        with connection.cursor() as cur:
            cur.execute(
                "SELECT encrypted_password FROM integrations_integrationconfig WHERE id = %s",
                [cfg.pk],
            )
            raw = cur.fetchone()[0]
        self.assertNotEqual(raw, "miSecreto")
        self.assertEqual(decrypt(raw), "miSecreto")

    def test_tolerates_legacy_plaintext(self):
        # Un valor que NO es token Fernet se devuelve tal cual (no revienta).
        self.assertEqual(decrypt("123"), "123")

    def test_blank_value_stays_blank(self):
        cfg = IntegrationConfig.objects.create(name="Vacio", system_type="DATAPARK")
        reloaded = IntegrationConfig.objects.get(pk=cfg.pk)
        self.assertEqual(reloaded.encrypted_password, "")


class EncryptionDisabledTests(TestCase):
    """Sin llave: el cifrado se deshabilita y nada se rompe."""

    @override_settings(FIELD_ENCRYPTION_KEY="")
    def test_no_key_behaves_as_plaintext(self):
        self.assertEqual(encrypt("abc"), "abc")
        self.assertEqual(decrypt("abc"), "abc")
