from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserLoginForm
from django.contrib.auth import login, authenticate, logout

def home_view(request):
    name = "Виктопус"
    context = {'name': 'Марынка'}
    return render(request, 'home.html', context )

def login_view(request):
    form = UserLoginForm(request.POST or None)
    next_ = request.GET.get('next')
    if form.is_valid():
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        user = authenticate(user_name=user_name.strip(), password=password.strip())
        login(request, user)
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or '/'
        return redirect(redirect_path)
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')