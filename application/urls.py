from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_landing, name='search_landing'),
]