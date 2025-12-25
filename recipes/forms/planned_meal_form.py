from django import forms
from recipes.helpers import visible_recipes_for
from datetime import date

class PlannedMealForm(forms.Form):
    """
    Form for adding a recipe to a planned day
    """
    MEAL_TYPES = [
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
        ("snack", "Snack"),
    ]
    
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        initial=date.today,
        required=False
    )
    
    meal_type = forms.ChoiceField(
        choices=MEAL_TYPES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    recipe = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    def __init__(self, *args, user=None, recipe=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["recipe"].queryset = visible_recipes_for(user)
        
        # If a recipe is provided, set it as the initial value
        if recipe:
            self.fields["recipe"].initial = recipe