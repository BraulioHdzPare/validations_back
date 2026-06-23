"""Prueba de conectividad contra Datapark (DpWebService).

Uso:
    python manage.py dp_ping
    python manage.py dp_ping --system-type DATAPARK

Llama a GetServiceVersion (conectividad + auth) y, de paso, a GetMerchants y
GetDiscounts para traer los MerchantKey / DiscountKey reales del sistema.
"""
from django.core.management.base import BaseCommand, CommandError

from apps.integrations.clients.datapark.client import DataparkClient
from apps.integrations.models import IntegrationConfig


class Command(BaseCommand):
    help = "Prueba de conectividad contra Datapark (GetServiceVersion, merchants, discounts)."

    def add_arguments(self, parser):
        parser.add_argument("--system-type", default="DATAPARK")

    def handle(self, *args, **options):
        config = (
            IntegrationConfig.objects.filter(
                system_type=options["system_type"], is_active=True
            )
            .order_by("id")
            .first()
        )
        if config is None:
            raise CommandError(
                f"No hay IntegrationConfig activo con system_type='{options['system_type']}'."
            )

        self.stdout.write(f"Conectando a {config.base_url} como '{config.username}'...")
        client = DataparkClient.from_config(config)

        version = client.get_service_version()
        self.stdout.write(self.style.SUCCESS(f"GetServiceVersion -> {version}"))

        try:
            merchants = client.get_merchants()
            self.stdout.write(f"GetMerchants -> {merchants}")
        except Exception as exc:  # noqa: BLE001 - diagnóstico
            self.stdout.write(self.style.WARNING(f"GetMerchants falló: {exc!r}"))

        try:
            discounts = client.get_discounts()
            self.stdout.write(f"GetDiscounts -> {discounts}")
        except Exception as exc:  # noqa: BLE001 - diagnóstico
            self.stdout.write(self.style.WARNING(f"GetDiscounts falló: {exc!r}"))
