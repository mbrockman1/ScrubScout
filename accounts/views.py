from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, TemplateView
from .models import CustomUser
from .forms import CustomUserCreationForm, ProfileForm
from reviews.models import Review

class SignupView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = '/'  # Redirect to homepage after signup
    success_message = 'Account created successfully!'

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user
        context['user_reviews'] = Review.objects.filter(author=self.request.user, is_hidden=False).order_by('-created_at')
        return context

class EditProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CustomUser
    form_class = ProfileForm
    template_name = 'accounts/edit_profile.html'
    success_url = '/accounts/profile/'
    success_message = 'Profile updated successfully!'

    def get_object(self):
        return self.request.user