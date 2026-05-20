from django.core.exceptions import ValidationError

from rest_framework.generics import GenericAPIView
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from api.models import Device

from api.services import WakeService

class WakeView(GenericAPIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, device_id):

        try:
            target_device = Device.objects.get(id=device_id)

            if target_device.user != request.user:
                return Response(
                    {"detail": "The requested resource is not accessible for you."},
                    status=status.HTTP_403_FORBIDDEN
                )

            WakeService.wake_device(target_device.mac) 

        except ValueError:
            return Response({"detail": f"Invalid MAC address format '{target_device.mac}'"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Device.DoesNotExist:
            return Response({"detail": f"No device with id '{device_id}' found."}, 
                status=status.HTTP_404_NOT_FOUND)

        return Response(
            {"detail": "Wake signal sent."},
            status=status.HTTP_200_OK,
        )