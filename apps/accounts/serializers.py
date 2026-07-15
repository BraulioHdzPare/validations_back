from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.accounts.models import User
from apps.parking_sites.models import ParkingSite
from apps.tenants.models import Tenant


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get("request"),
            username=attrs["username"],
            password=attrs["password"],
        )
        if not user:
            raise serializers.ValidationError("Credenciales inválidas.")
        if not user.is_active:
            raise serializers.ValidationError("Usuario inactivo.")
        attrs["user"] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    tenant_id = serializers.IntegerField(source="tenant.id", read_only=True, allow_null=True)
    tenant_name = serializers.CharField(source="tenant.name", read_only=True, allow_null=True)
    parking_site_id = serializers.IntegerField(source="parking_site.id", read_only=True, allow_null=True)
    parking_site_name = serializers.CharField(source="parking_site.name", read_only=True, allow_null=True)
    role_display = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "role_display",
            "tenant_id",
            "tenant_name",
            "parking_site_id",
            "parking_site_name",
        ]
        read_only_fields = fields


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Las contraseñas no coinciden."})
        return attrs


class UserManagementSerializer(serializers.ModelSerializer):
    """CRUD administrativo de usuarios (solo `admin`).

    La contraseña es de solo escritura: obligatoria al crear, opcional al
    editar (si se envía, reemplaza la actual). Nunca se devuelve en la
    respuesta.
    """

    password = serializers.CharField(
        write_only=True,
        required=False,
        style={"input_type": "password"},
    )
    tenant = serializers.PrimaryKeyRelatedField(
        queryset=Tenant.objects.all(),
        required=False,
        allow_null=True,
    )
    parking_site = serializers.PrimaryKeyRelatedField(
        queryset=ParkingSite.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "tenant",
            "parking_site",
            "is_active",
            "password",
        ]
        read_only_fields = ["id"]

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        # La contraseña solo es obligatoria al crear.
        if self.instance is None and not attrs.get("password"):
            raise serializers.ValidationError(
                {"password": "La contraseña es obligatoria al crear un usuario."}
            )
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save(update_fields=["password"])
        return user
