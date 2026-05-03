from rest_framework import serializers

from api.models import Device, User

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"
        read_only_fields = ["user"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "devices", "username", "first_name", "last_name", "email", "date_joined", "last_login", "is_superuser", "is_staff", "is_active"]
        read_only_fields = ["id", "username", "first_name", "last_name", "email", "date_joined", "last_login", "is_superuser", "is_staff", "is_active"]
