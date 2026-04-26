from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

@csrf_protect
@login_required(login_url='/login')
def index_view(request):
    return render(request, 'index.html')