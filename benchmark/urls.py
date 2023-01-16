from django.urls import path

from . import views

urlpatterns = [
    path('benchmark', views.benchmark, name='benchmark'),
    path('', views.index, name='index'),
]