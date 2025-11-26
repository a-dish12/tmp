from django import forms
from recipes.models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model=Recipe
        fields=['title','description','ingredients','time','meal_type']

        widgets={
            'description': forms.Textarea(attrs={
                'rows':4,
                'placeholder':"Describe your delicious recipe"
            }),
            'ingredients':forms.Textarea(attrs={
                'rows':6,
            }),
            'time': forms.NumberInput(attrs={
                'min':1,
                'placeholder':'30'
            }),
            'meal_type':forms.Textarea(attrs={
                'rows':4,
                'placeholder':'meal type'
            })
        }

        labels = {
            'title': 'Recipe Title',
            'description': 'Recipe Description',
            'ingredients': 'Ingredients List',
            'time': 'Preparation Time (minutes)',
            'meal_type':'meal type'
        }