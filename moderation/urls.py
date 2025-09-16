from django.urls import path
from . import views

urlpatterns = [
    path('report/<int:review_id>/', views.report_review, name='report_review'),  # FBV - no .as_view()
    path('dashboard/', views.StaffDashboard.as_view(), name='staff_dashboard'),  # CBV - has .as_view()
]