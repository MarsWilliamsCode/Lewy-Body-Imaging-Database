from django.urls import path
from . import views

urlpatterns = [
    path('', views.scan_list, name='scan_list'),
]