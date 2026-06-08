from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Only users with role=admin can access."""

    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated and request.user.is_admin)


class IsTenantUser(BasePermission):
    """Only users with role=tenant_user can access."""

    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated and request.user.is_tenant_user)


class IsAdminOrTenantUser(BasePermission):
    """Any authenticated user (admin or tenant_user)."""

    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in ("admin", "tenant_user")
        )
