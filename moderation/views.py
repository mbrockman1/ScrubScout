from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import ContentReport
from .forms import ReportForm

def report_review(request, review_id):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user  # Fixed: Use 'reporter' to match model
            report.review_id = review_id
            report.save()
            # Redirect back to place detail (you'll need to pass place_slug in context or use referer)
            return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = ReportForm()
    return render(request, 'moderation/report_form.html', {'form': form})

class StaffDashboard(UserPassesTestMixin, LoginRequiredMixin, TemplateView):  # FIXED: Subclass TemplateView
    template_name = 'moderation/dashboard.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reports'] = ContentReport.objects.filter(is_resolved=False)
        return context