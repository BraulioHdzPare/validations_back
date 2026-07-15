from rest_framework import viewsets

from apps.accounts.permissions import IsAdmin
from apps.tenants.models import Tenant
from apps.tenants.serializers import TenantSerializer


class TenantViewSet(viewsets.ModelViewSet):
    """CRUD administrativo de locatarios (solo `admin`).

    El borrado es lógico: `DELETE` desactiva (`is_active=False`) en lugar de
    eliminar, para preservar la trazabilidad (los `ValidationLog` referencian
    al tenant con `PROTECT`). Para reactivar: `PATCH {"is_active": true}`.
    """

    queryset = Tenant.objects.prefetch_related("parking_sites").all()
    serializer_class = TenantSerializer
    permission_classes = [IsAdmin]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=["is_active", "updated_at"])
