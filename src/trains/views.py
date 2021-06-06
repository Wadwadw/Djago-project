from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Train

def home(request):

    trains = Train.objects.all()
    paginator = Paginator(trains, 15)
    page = request.GET.get('page')
    trains = paginator.get_page(page)
    return render(request, 'trains/home.html', {'objects_list': trains, 'paginator': paginator})
