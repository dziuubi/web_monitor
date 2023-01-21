from django.contrib import admin
from django.urls import path, include
from web_monitor import views
urlpatterns = [
    path('benchmark/', include('benchmark.urls')),
    path('admin/', admin.site.urls),
    path('plot/', views.home, name='home'),
    path('checkfinish/', views.check_finish, name="check_finish"),
    path('report/<int:id>/', views.results, name="report"),
    path('', views.home, name='home')
]
