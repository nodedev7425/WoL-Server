from django.http import HttpResponse
from django.template import loader

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

@login_required(login_url='/login')
def index_view(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

@csrf_protect
def login_view(request):
    if request.method == "POST":
        print("Post")

    template = loader.get_template('login.html')
    return HttpResponse(template.render())