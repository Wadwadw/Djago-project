from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .models import City
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import CityForm
from django.contrib.messages.views import SuccessMessageMixin

def home(request):
    # if request.method == 'POST':
    #     form = CityForm(request.POST or None)
    #     if form.is_valid():
    #         print(form.cleaned_data)
    # form = CityForm()
    # city = request.POST.get('name')
    cities = City.objects.all()
    paginator = Paginator(cities, 15)
    page = request.GET.get('page')
    cities = paginator.get_page(page)
    return render(request, 'cities/home.html', {'objects_list': cities,})


class CityDetailView(DetailView):
    queryset = City.objects.all()
    context_object_name = 'object'
    template_name = 'cities/detail.html'

class CityCreateView(SuccessMessageMixin, CreateView):
    model = City
    form_class = CityForm
    template_name = 'cities/create.html'
    success_url = reverse_lazy('city:home')
    success_message = 'Город успешно создан'

class CityUpdateView(SuccessMessageMixin, UpdateView):
    model = City
    form_class = CityForm
    template_name = 'cities/update.html'
    success_url = reverse_lazy('city:home')
    success_message = 'Город успешно изменён'


class CityDeleteView(SuccessMessageMixin, DeleteView):
    model = City
    # template_name = 'cities/delete.html'
    success_url = reverse_lazy('city:home')
    success_message = 'Город успешно удалён'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

