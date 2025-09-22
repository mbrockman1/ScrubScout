from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'body', 'rating', 'pay_scale', 'housing_details']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'body': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'pay_scale': forms.TextInput(attrs={'class': 'form-control'}),
            'housing_details': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }