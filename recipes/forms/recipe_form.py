from django import forms
from recipes.models import Recipe


class RecipeForm(forms.ModelForm):
    meal_types = forms.ChoiceField(
        choices=Recipe.MEAL_TYPE_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        label='Meal Types'
    )
    
    # Number of ingredient and instruction fields to show
    ingredient_count = forms.IntegerField(widget=forms.HiddenInput(), initial=1, required=False)
    instruction_count = forms.IntegerField(widget=forms.HiddenInput(), initial=1, required=False)
    
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'time', 'image', 'image_url']

        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': "Describe your delicious recipe"
            }),
            'time': forms.NumberInput(attrs={
                'min': 1,
                'placeholder': '30'
            }),
            'image_url': forms.URLInput(attrs={
                'placeholder': 'https://example.com/image.jpg'
            })
        }

        labels = {
            'title': 'Recipe Title',
            'description': 'Recipe Description',
            'time': 'Preparation Time (minutes)',
            'image': 'Upload Image (optional)',
            'image_url': 'Or Image URL (optional)'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If editing an existing recipe, populate meal_types from meal_type
        if self.instance and self.instance.pk and self.instance.meal_type:
            # Take the first meal type since we now only allow one
            meal_types_list = [mt.strip() for mt in self.instance.meal_type.split(',')]
            self.fields['meal_types'].initial = meal_types_list[0] if meal_types_list else None
        
        # Get number of fields from POST data or instance
        if self.data:
            ingredient_count = int(self.data.get('ingredient_count', 1))
            instruction_count = int(self.data.get('instruction_count', 1))
        elif self.instance and self.instance.pk:
            # For editing, count existing items
            ingredient_count = len(self.instance.get_ingredients_list()) or 1
            instruction_count = len(self.instance.get_instructions_list()) or 1
        else:
            ingredient_count = 1
            instruction_count = 1
        
        self.fields['ingredient_count'].initial = ingredient_count
        self.fields['instruction_count'].initial = instruction_count
        
        # Create dynamic ingredient fields
        for i in range(ingredient_count):
            field_name = f'ingredient_{i}'
            self.fields[field_name] = forms.CharField(
                required=False,
                widget=forms.TextInput(attrs={
                    'placeholder': 'e.g., 2 cups flour',
                    'class': 'form-control'
                }),
                label=''
            )
            # Populate with existing data if editing
            if self.instance and self.instance.pk:
                ingredients_list = self.instance.get_ingredients_list()
                if i < len(ingredients_list):
                    self.fields[field_name].initial = ingredients_list[i]
        
        # Create dynamic instruction fields
        for i in range(instruction_count):
            field_name = f'instruction_{i}'
            self.fields[field_name] = forms.CharField(
                required=False,
                widget=forms.Textarea(attrs={
                    'rows': 2,
                    'placeholder': 'e.g., Preheat oven to 350°F',
                    'class': 'form-control'
                }),
                label=''
            )
            # Populate with existing data if editing
            if self.instance and self.instance.pk:
                instructions_list = self.instance.get_instructions_list()
                if i < len(instructions_list):
                    self.fields[field_name].initial = instructions_list[i]
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Convert meal_types single choice to meal_type
        meal_type = cleaned_data.get('meal_types', '')
        if meal_type:
            cleaned_data['meal_type'] = meal_type
        
        # Collect ingredients
        ingredient_count = int(self.data.get('ingredient_count', 1))
        ingredients = []
        for i in range(ingredient_count):
            ingredient = cleaned_data.get(f'ingredient_{i}', '').strip()
            if ingredient:
                ingredients.append(ingredient)
        
        if not ingredients:
            raise forms.ValidationError('Please add at least one ingredient.')
        
        cleaned_data['ingredients'] = '\n'.join(ingredients)
        
        # Collect instructions
        instruction_count = int(self.data.get('instruction_count', 1))
        instructions = []
        for i in range(instruction_count):
            instruction = cleaned_data.get(f'instruction_{i}', '').strip()
            if instruction:
                instructions.append(instruction)
        
        if not instructions:
            raise forms.ValidationError('Please add at least one instruction.')
        
        cleaned_data['instructions'] = '\n'.join(instructions)
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.meal_type = self.cleaned_data['meal_type']
        instance.ingredients = self.cleaned_data['ingredients']
        instance.instructions = self.cleaned_data['instructions']
        
        if commit:
            instance.save()
        return instance