from recipes.constants.filters import MEAL_TYPES, TIME_FILTERS
from django import forms
""", DIET_FILTERS"""

class SurpriseMeForm(forms.Form):



    meal_type = forms.MultipleChoiceField(
        choices = MEAL_TYPES,
        widget = forms.CheckboxSelectMultiple,
        required = False,
    )

    time_filter = forms.ChoiceField(
        choices = TIME_FILTERS,
        widget = forms.RadioSelect,
        required = False,
      
    )

"""    diet_filter = forms.ChoiceField(
        choices = DIET_FILTERS,
        widget = forms.RadioSelect,
        required = True
    )"""