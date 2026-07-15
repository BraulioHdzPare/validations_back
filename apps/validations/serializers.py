from rest_framework import serializers

from apps.parking_sites.models import ParkingSite
from apps.tenants.models import Tenant
from apps.validations.models import ValidationType


class TicketLookupRequestSerializer(serializers.Serializer):
    parking_site_id = serializers.IntegerField()
    ticket_number = serializers.CharField(max_length=100)

class ApplyValidationRequestSerializer(serializers.Serializer):
    parking_site_id = serializers.IntegerField()
    ticket_number = serializers.CharField(max_length=100)
    validation_code = serializers.CharField(max_length=50)


class ValidationTypeSerializer(serializers.ModelSerializer):
    """Serializer de gestión (CRUD administrativo) de los descuentos/validaciones.

    `parking_sites` y `tenants` se asignan por sus IDs; ambos son opcionales
    (un descuento puede crearse y asociarse después).
    """

    parking_sites = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=ParkingSite.objects.all(),
        required=False,
    )
    tenants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tenant.objects.all(),
        required=False,
    )

    class Meta:
        model = ValidationType
        fields = [
            "id",
            "name",
            "code",
            "external_code",
            "description",
            "is_active",
            "parking_sites",
            "tenants",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]