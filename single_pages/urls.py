from django.urls import path, include
from . import views


urlpatterns = [
    path('', include('admin_adminlte.urls')), 
    path('about/', views.about),
    path('', views.landing),
]