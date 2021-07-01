"""trawel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from routs.views import home, find_routs, add_route, RouteListlView, RouteDetailView, RouteDeleteView
from .views import login_view, logout_view, register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cities/', include(('cities.urls', 'city'))),
    path('trains/', include(('trains.urls', 'train'))),
    path('find/', find_routs, name='find_routs'),
    path('add_route/', add_route, name='add_route'),
    path('list/', RouteListlView.as_view(), name='list'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('detail/<int:pk>/', RouteDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', RouteDeleteView.as_view(), name='delete'),
    path('', home, name='home'),

]
