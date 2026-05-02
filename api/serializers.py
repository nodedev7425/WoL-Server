from rest_framework import serializers

from api.models import Device

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ["id", "name", "mac", "last_wake", "created"]