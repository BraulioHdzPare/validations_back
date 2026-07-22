from django.test import TestCase
from rest_framework.exceptions import NotFound

from apps.accounts.models import User
from apps.integrations.models import IntegrationConfig
from apps.parking_sites.models import ParkingSite
from apps.tenants.models import Tenant
from apps.validations.models import ValidationLog, ValidationType
from apps.validations.services import ApplyValidationService


class ApplyValidationTenantScopeTests(TestCase):
    """Regla de negocio de seguridad: un ``tenant_user`` solo puede aplicar
    validaciones autorizadas para SU locatario.

    Cubre la asimetría que fue el bug hasta 0.4: ``TicketLookupService`` filtraba
    por ``tenant`` pero ``ApplyValidationService`` no, así que un ``tenant_user``
    podía aplicar un descuento ajeno conociendo su ``code``. Este test evita que
    una futura refactorización reintroduzca el hueco en silencio.
    """

    @classmethod
    def setUpTestData(cls):
        # Integración DESIGNA: su provider es un mock, no hace llamadas externas.
        integration = IntegrationConfig.objects.create(
            name="Designa Test",
            system_type=IntegrationConfig.SYSTEM_DESIGNA,
        )
        cls.parking_site = ParkingSite.objects.create(
            name="Unidad Centro",
            code="UC-01",
            integration=integration,
        )

        cls.tenant_a = Tenant.objects.create(name="Locatario A")
        cls.tenant_b = Tenant.objects.create(name="Locatario B")

        # La validación está autorizada para la unidad y SOLO para el tenant A.
        cls.validation = ValidationType.objects.create(
            name="Cortesía 2h",
            code="CORT2H",
            external_code="5",
        )
        cls.validation.parking_sites.add(cls.parking_site)
        cls.validation.tenants.add(cls.tenant_a)

        cls.user_a = User.objects.create_user(
            username="loc_a",
            password="pass12345",
            role=User.Role.TENANT_USER,
            tenant=cls.tenant_a,
            parking_site=cls.parking_site,
        )
        cls.user_b = User.objects.create_user(
            username="loc_b",
            password="pass12345",
            role=User.Role.TENANT_USER,
            tenant=cls.tenant_b,
            parking_site=cls.parking_site,
        )
        cls.admin = User.objects.create_user(
            username="admin1",
            password="pass12345",
            role=User.Role.ADMIN,
        )

    def _apply(self, user):
        return ApplyValidationService().execute(
            user=user,
            parking_site_id=self.parking_site.id,
            ticket_number="T-001",
            validation_code=self.validation.code,
        )

    def test_tenant_user_cannot_apply_other_tenants_validation(self):
        # user_b pertenece al tenant B; la validación es solo del tenant A.
        with self.assertRaises(NotFound):
            self._apply(self.user_b)
        # No debe registrarse ningún intento: se rechaza antes de llamar al proveedor.
        self.assertFalse(ValidationLog.objects.exists())

    def test_tenant_user_can_apply_own_tenants_validation(self):
        # Guard contra sobre-bloqueo: el locatario autorizado sí debe poder aplicar.
        result = self._apply(self.user_a)
        self.assertTrue(result.success)
        self.assertEqual(ValidationLog.objects.count(), 1)

    def test_admin_is_not_restricted_by_tenant(self):
        # El admin no tiene tenant: aplica cualquier validación de la unidad.
        result = self._apply(self.admin)
        self.assertTrue(result.success)
