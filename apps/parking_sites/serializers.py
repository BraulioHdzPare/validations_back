from rest_framework import serializers
from apps.parking_sites.models import ParkingSite

class ParkingSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSite
        fields = [
            'id',
            'name',
            'code',
            'is_active',
        ]