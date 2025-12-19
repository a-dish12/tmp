from django import forms
from recipes.models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model=Recipe
        fields=['title','description','ingredients','instructions','time','meal_type','image','image_url']

        widgets={
            'description': forms.Textarea(attrs={
                'rows':4,
                'placeholder':"Describe your delicious recipe"
            }),
            'ingredients':forms.Textarea(attrs={
                'rows':6,
                'placeholder':'List all ingredients'
            }),
            'instructions':forms.Textarea(attrs={
                'rows':8,
                'placeholder':'1. Preheat oven to 350°F\n2. Mix ingredients...'
            }),
            'time': forms.NumberInput(attrs={
                'min':1,
                'placeholder':'30'
            }),
            'meal_type':forms.Textarea(attrs={
                'rows':4,
                'placeholder':'meal type'
            }),
            'image_url': forms.URLInput(attrs={
                'placeholder':'https://example.com/image.jpg'
            })
        }

        labels = {
            'title': 'Recipe Title',
            'description': 'Recipe Description',
            'ingredients': 'Ingredients List',
            'instructions': 'Cooking Instructions',
            'time': 'Preparation Time (minutes)',
            'meal_type':'meal type',
            'image': 'Upload Image (optional)',
            'image_url': 'Or Image URL (optional)'
        }