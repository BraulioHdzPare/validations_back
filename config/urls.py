from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.accounts.views import UserViewSet
from apps.parking_sites.views import ParkingSiteViewSet
from apps.tenants.views import TenantViewSet
from apps.validations.views import ValidationTypeViewSet

router = DefaultRouter()
router.register(
    r"validation-types",
    ValidationTypeViewSet,
    basename="validation-type",
)
router.register(
    r"tenants",
    TenantViewSet,
    basename="tenant",
)
router.register(
    r"users",
    UserViewSet,
    basename="user",
)
router.register(
    r"parking-sites",
    ParkingSiteViewSet,
    basename="parking-site",
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/validations/", include("apps.validations.urls")),
    path("api/admin/", include(router.urls)),
]

# Debug toolbar solo en desarrollo
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
