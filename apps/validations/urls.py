from django.urls import path
from apps.validations.views import TicketLookupAPIView, ApplyValidationAPIView


urlpatterns = [
    path('tickets/lookup/', TicketLookupAPIView.as_view(), name='ticket-lookup'),
    path('apply/', ApplyValidationAPIView.as_view(), name='apply-validation'),
]