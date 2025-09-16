from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>/', views.place_detail, name='place_detail'),
]