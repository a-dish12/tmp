from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from recipes.models import Recipe
from recipes.forms import RecipeForm

class EditRecipeView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for editing an existing recipe. Only the author can edit."""
    model = Recipe
    form_class = RecipeForm
    template_name = 'edit_recipe.html'
    
    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        form.instance.meal_type = form.instance.meal_type.strip().lower()
        return super().form_valid(form)
    
    def test_func(self):
        """Check that the current user is the recipe author."""
        recipe = self.get_object()
        return self.request.user == recipe.author


class DeleteRecipeView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting a recipe. Only the author can delete."""
    model = Recipe
    template_name = 'delete_recipe.html'
    success_url = reverse_lazy('user_recipes')
    
    def test_func(self):
        """Check that the current user is the recipe author."""
        recipe = self.get_object()
        return self.request.user == recipe.author
