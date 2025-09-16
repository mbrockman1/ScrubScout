from django.urls import path
from . import views

urlpatterns = [
    path('places/<slug:slug>/review/new/', views.CreateReviewView.as_view(), name='create_review'),
    path('review/<int:review_id>/edit/', views.UpdateReviewView.as_view(), name='edit_review'),
]