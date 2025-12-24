from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views import View
from recipes.models import Recipe
from recipes.forms.recipe_form import RecipeForm


class CreateRecipeView(LoginRequiredMixin, View):
    template_name = 'create_recipe.html'

    def get(self, request):
        form = RecipeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # Check if user wants to add more fields
        if 'add_ingredient' in request.POST:
            data = request.POST.copy()
            data['ingredient_count'] = int(data.get('ingredient_count', 1)) + 1
            form = RecipeForm(data=data, files=request.FILES)
            return render(request, self.template_name, {'form': form})
        
        if 'add_instruction' in request.POST:
            data = request.POST.copy()
            data['instruction_count'] = int(data.get('instruction_count', 1)) + 1
            form = RecipeForm(data=data, files=request.FILES)
            return render(request, self.template_name, {'form': form})
        
        # Check if user wants to remove fields (but keep at least 1)
        if 'remove_ingredient' in request.POST:
            data = request.POST.copy()
            current_count = int(data.get('ingredient_count', 1))
            if current_count > 1:
                data['ingredient_count'] = current_count - 1
            form = RecipeForm(data=data, files=request.FILES)
            return render(request, self.template_name, {'form': form})
        
        if 'remove_instruction' in request.POST:
            data = request.POST.copy()
            current_count = int(data.get('instruction_count', 1))
            if current_count > 1:
                data['instruction_count'] = current_count - 1
            form = RecipeForm(data=data, files=request.FILES)
            return render(request, self.template_name, {'form': form})

        # Normal form submission
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('user_recipes')

        return render(request, self.template_name, {'form': form})