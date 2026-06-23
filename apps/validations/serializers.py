from rest_framework import serializers

class TicketLookupRequestSerializer(serializers.Serializer):
    parking_site_id = serializers.IntegerField()
    ticket_number = serializers.CharField(max_length=100)

class ApplyValidationRequestSerializer(serializers.Serializer):
    parking_site_id = serializers.IntegerField()
    ticket_number = serializers.CharField(max_length=100)
    validation_code = serializers.CharField(max_length=50)