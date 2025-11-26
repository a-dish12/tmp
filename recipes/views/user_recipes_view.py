from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from recipes.models import Recipe


class UserRecipesView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'user_recipes.html'
    context_object_name = 'recipes'
    
    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)