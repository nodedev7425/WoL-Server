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

        if request.user.is_authenticated:
            return redirect(request.POST['next'])

        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(request.POST['next'])
            else:
                return JsonResponse({'error': 'Authentication failed'}, status=401)

        next_url = request.GET.get('next', '')
        return render(request, 'login.html', { 'next': next_url })