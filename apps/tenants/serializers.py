from rest_framework import serializers

from apps.parking_sites.models import ParkingSite
from apps.tenants.models import Tenant


class TenantSerializer(serializers.ModelSerializer):
    """Serializer de gestión (CRUD administrativo) de locatarios.

    `parking_sites` se asigna por IDs y es opcional (un locatario puede crearse
    y asociarse a unidades después).
    """

    parking_sites = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=ParkingSite.objects.all(),
        required=False,
    )

    class Meta:
        model = Tenant
        fields = [
            "id",
            "name",
            "trade_name",
            "is_active",
            "parking_sites",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
