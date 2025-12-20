from django import forms
from recipes.models import Rating

class RatingForm(forms.ModelForm):
    """Form for rating a recipe with star selection."""
    
    STAR_CHOICES = [(i, f'{i} star{"s" if i > 1 else ""}') for i in range(1, 6)]
    
    stars = forms.ChoiceField(
        choices=STAR_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'star-rating-radio'}),
        label="Rate this recipe"
    )
    
    class Meta:
        model = Rating
        fields = ['stars']
