from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import DetailView
from .models import Train
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .forms import TrainForm



def home(request):

    trains = Train.objects.all()
    paginator = Paginator(trains, 10)

    page = request.GET.get('page')
    trains = paginator.get_page(page)
    return render(request, 'trains/home.html', {'objects_list': trains, 'paginator': paginator})

class TrainCreateView(SuccessMessageMixin, CreateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/create.html'
    success_url = reverse_lazy('train:home')
    success_message = 'Поезд успешно создан'

class TrainDetailView(DetailView):
    queryset = Train.objects.all()
    context_object_name = 'object'
    template_name = 'trains/detail.html'



class TrainUpdateView(SuccessMessageMixin, UpdateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/update.html'
    success_url = reverse_lazy('train:home')
    success_message = 'Поезд успешно изменён'


class TrainDeleteView(SuccessMessageMixin, DeleteView):
    model = Train
    # template_name = 'cities/delete.html'
    success_url = reverse_lazy('train:home')
    success_message = 'Поезд успешно удалён'

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Поезд успешно удалён')
        return self.post(request, *args, **kwargs)

