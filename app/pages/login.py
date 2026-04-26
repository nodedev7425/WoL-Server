from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login

from django.views.decorators.csrf import csrf_protect

@csrf_protect
def login_view(request):
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