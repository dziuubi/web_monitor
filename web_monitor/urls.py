from django.contrib import admin
from django.urls import path, include
from web_monitor import views
urlpatterns = [
    path('benchmark/', include('benchmark.urls')),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('plot/', views.home, name='home')
]
