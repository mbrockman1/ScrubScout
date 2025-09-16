from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_results, name='search_results'),  # /search/ → results page
]