from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView
from django.urls import reverse
from .models import Review
from .forms import ReviewForm
from places.models import Place
from django.db import models
from django.conf import settings


class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.place = get_object_or_404(Place, slug=self.kwargs['slug'])
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.place.get_absolute_url()

class UpdateReviewView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'
    pk_url_kwarg = 'review_id'

    def get_queryset(self):
        # Only allow editing own reviews
        return Review.objects.filter(user=self.request.user)

    def get_success_url(self):
        return self.object.place.get_absolute_url()
    