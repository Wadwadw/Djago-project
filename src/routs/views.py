from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from trains.models import Train
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def dfs_paths(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))
def get_graph():
    qs = Train.objects.values('from_city')
    from_city_set = set(i['from_city'] for i in qs)
    graph = {}
    for city in from_city_set:
        trains = Train.objects.filter(from_city=city).values('to_city')
        tmp = set(i['to_city'] for i in trains)
        graph[city] = tmp
    return graph


# @login_required(login_url='/login/')
def home(request):
    form = RouteForm()
    return render(request, 'routs/home.html', {'form': form})


def find_routs(request):
    if request.method == 'POST':
        form = RouteForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            # assert False
            from_city = data['from_city']
            to_city = data['to_city']
            across_cities_form = data['across_cities']
            traveling_time = data['travel_time']
            graph = get_graph()
            all_ways = list(dfs_paths(graph, from_city.id, to_city.id))
            if len(all_ways) == 0:
                messages.error(request, 'Маршрута, удовлетворяющего условиям не существует')
                return render(request, 'routs/home.html', {'form': form})
            if across_cities_form:
                across_cities = [city.id for city in across_cities_form]
                right_ways = []
                for way in all_ways:
                    if all(point in way for point in across_cities):
                        right_ways.append(way)
                if not right_ways:
                    messages.error(request, 'Маршрут через эти города невозможен')
                    return render(request, 'routs/home.html', {'form': form})
            else:
                right_ways = all_ways

            trains = []
            for route in right_ways:
                tmp = {}
                tmp['trains'] = []
                total_time = 0
                for index in range(len(route)-1):
                    qs = Train.objects.filter(from_city=route[index], to_city=route[index+1])
                    qs = qs.order_by('travel_time').first()
                    total_time += qs.travel_time
                    tmp['trains'].append(qs)
                tmp['total_time'] = total_time
                if total_time <= int(traveling_time):
                    trains.append(tmp)
            if not trains:
                messages.error(request, 'Время в пути больше заданного')
                return render(request, 'routs/home.html', {'form': form})

            routes = []
            cities = {'from_city': from_city.name, 'to_city': to_city.name}
            for tr in trains :
                routes.append({'route': tr['trains'],
                               'total_time': tr['total_time'],
                               'from_city': from_city.name,
                               'to_city': to_city.name,
                               })
            sorted_routes = []
            if len(routes) == 1:
                sorted_routes = routes
            else:
                times = list(set(x['total_time'] for x in routes))
                times = sorted(times)
                for time in times:
                    for route in routes:
                        if time == route['total_time']:
                            sorted_routes.append(route)

            context = {}
            form = RouteForm()
            context['form'] = form
            context['ways'] = trains
            context['routes'] = sorted_routes
            context['cities'] = cities
            return render(request, 'routs/home.html', context)
        return render(request, 'routs/home.html', {'form': form})
    else:
        messages.error(request, 'Создайте маршрут')
        form = RouteForm()
        return render(request, 'routs/home.html', {'form': form})

def add_route(request):
    if request.method == 'POST':
        form = RouteModelForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            name = data['name']
            travel_times = data['travel_times']
            from_city = data['from_city']
            to_city = data['to_city']
            across_cities = data['across_cities'].split(' ')
            trains = [int(x) for x in across_cities if x.isalnum()]
            qs = Train.objects.filter(id__in=trains)
            route = Route(name=name, from_city=from_city,
                          to_city=to_city, travel_times=travel_times
                          )
            route.save()
            for tr in qs:
                route.across_cities.add(tr.id)
            messages.success(request, 'Маршрут успешно сохранён')
            return redirect('/')
    else:
        data = request.GET
        if data:
            travel_times = data['travel_time']
            from_city = data['from_city']
            to_city = data['to_city']
            across_cities = data['across_city'].split(' ')
            trains = [int(x) for x in across_cities if x.isalnum()]
            qs = Train.objects.filter(id__in=trains)
            train_list = ' '.join(str(i) for i in trains)
            form = RouteModelForm(initial={
                'from_city': from_city,
                'to_city': to_city,
                'travel_times': travel_times,
                'across_cities': train_list,
            })
            route_desc = []
            for tr in qs:
                dsc = f'Поезд №{tr.name} следующий из г.{tr.from_city} в г.{tr.to_city}. Времяв пути {tr.travel_time} '
                route_desc.append(dsc)

            context = {
                'form': form,
                'descr': route_desc,
                'from_city': from_city,
                'to_city': to_city,
                'travel_times': travel_times,
            }

            # assert False
            return render(request, 'routs/create.html', context)
        else:
            messages.error(request, 'Невозможно сохранить несуществующий маршрут')
            return redirect('/')

class RouteDetailView(DetailView):
    queryset = Route.objects.all()
    context_object_name = 'object'
    template_name = 'routs/detail.html'

class RouteListlView(ListView):
    queryset = Route.objects.all()
    context_object_name = 'objects_list'
    template_name = 'routs/list.html'

class RouteDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Route
    # template_name = 'routes/list.html'
    success_url = reverse_lazy('home')
    success_message = 'Маршрут успешно удалён'
    login_url = '/login/'
    def get(self, request, *args, **kwargs):
        messages.success(request, 'Маршрут успешно удалён')
        return self.post(request, *args, **kwargs)
