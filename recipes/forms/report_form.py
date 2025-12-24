"""Forms for reporting content."""
from django import forms
from recipes.models import Report


class ReportForm(forms.ModelForm):
    """Form for reporting recipes or comments."""
    
    class Meta:
        model = Report
        fields = ['reason', 'description']
        widgets = {
            'reason': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Please provide specific details about why you are reporting this content...',
                'required': True
            })
        }
        labels = {
            'reason': 'Reason for reporting',
            'description': 'Additional details'
        }
