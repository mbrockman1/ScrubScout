from django.urls import path
from .views import moderator_dashboard, deactivate_user, hide_review, unhide_review, delete_review

urlpatterns = [
    path('dashboard/', moderator_dashboard, name='moderator_dashboard'),
    path('user/<int:user_id>/deactivate/', deactivate_user, name='deactivate_user'),
    path('review/<int:review_id>/hide/', hide_review, name='hide_review'),
    path('review/<int:review_id>/unhide/', unhide_review, name='unhide_review'),
    path('review/<int:review_id>/delete/', delete_review, name='delete_review'),
]