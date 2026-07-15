from rest_framework import viewsets

from apps.accounts.permissions import IsAdmin
from apps.parking_sites.models import ParkingSite
from apps.parking_sites.serializers import ParkingSiteSerializer


class ParkingSiteViewSet(viewsets.ReadOnlyModelViewSet):
    """Listado/lectura de unidades de estacionamiento (solo `admin`).

    De momento solo lectura: alimenta los selectores de los formularios de
    descuentos, locatarios y usuarios. La gestión completa de unidades (que
    implica elegir su `IntegrationConfig`) se aborda por separado.
    """

    queryset = ParkingSite.objects.all()
    serializer_class = ParkingSiteSerializer
    permission_classes = [IsAdmin]
