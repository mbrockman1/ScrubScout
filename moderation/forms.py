from django import forms
from .models import ContentReport

class ReportForm(forms.ModelForm):
    class Meta:
        model = ContentReport
        fields = ['reason', 'description']
        widgets = {
            'reason': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }