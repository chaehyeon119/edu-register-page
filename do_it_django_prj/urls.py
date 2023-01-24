from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('edu/', include('edu.urls')),
    path("admin/", admin.site.urls),
]
