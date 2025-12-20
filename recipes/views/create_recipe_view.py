from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from recipes.models import Recipe
from recipes.forms import RecipeForm

class CreateRecipeView(LoginRequiredMixin,CreateView):
    model=Recipe
    form_class=RecipeForm
    template_name='create_recipe.html'
    success_url=reverse_lazy('user_recipes')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.meal_type = form.instance.meal_type.strip().lower()
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # This ensures file uploads work properly
        return kwargs

    