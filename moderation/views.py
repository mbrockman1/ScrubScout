from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.conf import settings
from .models import ContentReport, ModerationAction
from reviews.models import Review
from django.contrib import messages

@staff_member_required
def deactivate_user(request, user_id):
    user = get_object_or_404(settings.AUTH_USER_MODEL, id=user_id)
    if request.method == 'POST':
        user.is_active = False
        user.save()
        messages.success(request, f"User {user.display_name} deactivated.")
        return redirect('admin:auth_user_changelist')
    return render(request, 'moderation/deactivate_user.html', {'target_user': user})

@staff_member_required
def moderator_dashboard(request):
    pending_reports = ContentReport.objects.filter(is_resolved=False).order_by('-created_at')[:10]
    recent_actions = ModerationAction.objects.all().order_by('-created_at')[:10]
    context = {
        'pending_reports': pending_reports,
        'recent_actions': recent_actions,
    }
    return render(request, 'moderation/dashboard.html', context)

@staff_member_required
def hide_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        review.is_hidden = True
        review.save()
        ModerationAction.objects.create(
            staff=request.user,
            review=review,
            action='hidden',
            notes='Hidden via dashboard'
        )
        messages.success(request, f"Review '{review.title}' hidden.")
        return redirect('moderator_dashboard')
    return render(request, 'moderation/hide_review.html', {'review': review})

@staff_member_required
def unhide_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        review.is_hidden = False
        review.save()
        ModerationAction.objects.create(
            staff=request.user,
            review=review,
            action='restored',
            notes='Restored via dashboard'
        )
        messages.success(request, f"Review '{review.title}' restored.")
        return redirect('moderator_dashboard')
    return render(request, 'moderation/unhide_review.html', {'review': review})

@staff_member_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        ModerationAction.objects.create(
            staff=request.user,
            review=review,
            action='deleted',
            notes='Deleted via dashboard'
        )
        review.delete()
        messages.success(request, f"Review deleted.")
        return redirect('moderator_dashboard')
    return render(request, 'moderation/delete_review.html', {'review': review})