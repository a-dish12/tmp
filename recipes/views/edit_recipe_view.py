from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from recipes.models import Recipe
from recipes.forms import RecipeForm


class EditRecipeView(LoginRequiredMixin, UserPassesTestMixin, View):
    """View for editing an existing recipe. Only the author can edit."""
    template_name = 'edit_recipe.html'

    def get_object(self):
        return get_object_or_404(Recipe, pk=self.kwargs['pk'])
    
    def test_func(self):
        """Check that the current user is the recipe author."""
        recipe = self.get_object()
        return self.request.user == recipe.author
    
    def dispatch(self, request, *args, **kwargs):
        """Override dispatch to perform the test_func check."""
        if not self.test_func():
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        recipe = self.get_object()
        form = RecipeForm(instance=recipe)
        return render(request, self.template_name, {'form': form, 'recipe': recipe})

    def post(self, request, pk):
        recipe = self.get_object()
        
        # Check if user wants to add more fields
        if 'add_ingredient' in request.POST:
            data = request.POST.copy()
            data['ingredient_count'] = int(data.get('ingredient_count', 1)) + 1
            form = RecipeForm(data=data, files=request.FILES, instance=recipe)
            return render(request, self.template_name, {'form': form, 'recipe': recipe})
        
        if 'add_instruction' in request.POST:
            data = request.POST.copy()
            data['instruction_count'] = int(data.get('instruction_count', 1)) + 1
            form = RecipeForm(data=data, files=request.FILES, instance=recipe)
            return render(request, self.template_name, {'form': form, 'recipe': recipe})
        
        # Check if user wants to remove fields (but keep at least 1)
        if 'remove_ingredient' in request.POST:
            data = request.POST.copy()
            current_count = int(data.get('ingredient_count', 1))
            if current_count > 1:
                data['ingredient_count'] = current_count - 1
            form = RecipeForm(data=data, files=request.FILES, instance=recipe)
            return render(request, self.template_name, {'form': form, 'recipe': recipe})
        
        if 'remove_instruction' in request.POST:
            data = request.POST.copy()
            current_count = int(data.get('instruction_count', 1))
            if current_count > 1:
                data['instruction_count'] = current_count - 1
            form = RecipeForm(data=data, files=request.FILES, instance=recipe)
            return render(request, self.template_name, {'form': form, 'recipe': recipe})

        # Normal form submission
        form = RecipeForm(request.POST, request.FILES, instance=recipe)

        if form.is_valid():
            form.save()
            return redirect('recipe_detail', pk=recipe.pk)

        return render(request, self.template_name, {'form': form, 'recipe': recipe})


class DeleteRecipeView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting a recipe. Only the author can delete."""
    model = Recipe
    template_name = 'delete_recipe.html'
    success_url = reverse_lazy('user_recipes')
    
    def test_func(self):
        """Check that the current user is the recipe author."""
        recipe = self.get_object()
        return self.request.user == recipe.author
