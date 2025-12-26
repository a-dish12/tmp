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
    
    def clean(self):
        cleaned_data = super().clean()
        reason = cleaned_data.get('reason')
        description = cleaned_data.get('description')
        
        if not reason or not description:
            raise forms.ValidationError('Please provide both a reason and description for your report.')
        
        return cleaned_data
