from django import forms
from recipes.helpers import visible_recipes_for

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

    meal_type = forms.ChoiceField(choices=MEAL_TYPES)
    recipe = forms.ModelChoiceField(queryset=None)
    
    """
    """
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["recipe"].queryset = visible_recipes_for(user)