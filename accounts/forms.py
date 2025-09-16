from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    display_name = forms.CharField(max_length=100, required=False, help_text="Optional display name")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'display_name', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['display_name', 'avatar', 'bio', 'location']