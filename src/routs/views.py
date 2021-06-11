from django.shortcuts import render
from .forms import *

def home(request):
    form = RouteForm()
    return render(request, 'routs/home.html', {'form': form})



