from django.urls import path
from .views import CreateReviewView, UpdateReviewView, ReviewDetailView, DeleteReviewView

urlpatterns = [
    path('create/<slug:slug>/', CreateReviewView.as_view(), name='review_create'),
    path('<int:review_id>/', ReviewDetailView.as_view(), name='review_detail'),
    path('<int:review_id>/edit/', UpdateReviewView.as_view(), name='review_edit'),
    path('<int:review_id>/delete/', DeleteReviewView.as_view(), name='review_delete'),
]