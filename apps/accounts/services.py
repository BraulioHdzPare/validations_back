from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import User


class AuthService:
    @staticmethod
    def issue_tokens(user: User) -> dict:
        """Return access + refresh JWT pair for the given user."""
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

    @staticmethod
    def change_password(user: User, current_password: str, new_password: str) -> None:
        if not user.check_password(current_password):
            from rest_framework import serializers
            raise serializers.ValidationError({"current_password": "Contraseña actual incorrecta."})
        user.set_password(new_password)
        user.save(update_fields=["password"])
