from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_landing, name='search_landing'),
    path("search/", views.search_results, name="search_results"),
    path("search/scan/<str:scan_id>", views.scan_page, name="scan_id"),
]