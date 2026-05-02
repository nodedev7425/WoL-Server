from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import DeviceSerializer

class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="me/devices")
    def devices(self, request):
        devices = request.user.devices.all()
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)