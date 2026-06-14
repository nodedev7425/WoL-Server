from django.views import View
from django.http import JsonResponse
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

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

    def post(self, request, *args, **kwargs):
        
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.POST['next'])
        else:
            return JsonResponse({'error': 'Authentication failed'}, status=401)

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect(request.GET.get('next', '/'))


        next_url = request.GET.get('next', '/')
        return render(request, 'login.html', { 'next': next_url })