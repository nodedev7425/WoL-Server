from django.views import View
from django.shortcuts import render 

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect

from api.serializers import DeviceSerializer

class IndexView(LoginRequiredMixin, View):

    login_url = "/login/"

    def get(self, request, *args, **kwargs):

        context = {
            "devices": DeviceSerializer(
                request.user.devices.all(),
                many=True
            ).data
        }

        return render(request, "index.html", context) 

class LoginView(View):

    @csrf_protect
    def get(self, request, *args, **kwargs):
        return render(request, "login.html") 