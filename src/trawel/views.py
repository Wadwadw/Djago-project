from django.http import HttpResponse
from django.shortcuts import render

def home_view(request):
    name = "Виктопус"
    context = {'name': 'Марынка'}
    return render(request, 'home.html', context )