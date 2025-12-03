from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from recipes.models import Recipe, Rating


class RecipeDetailView(DetailView):
    """Display full recipe details with rating."""
    
    model = Recipe
    template_name = 'recipe_detail.html'
    context_object_name = 'recipe'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add user's rating if authenticated
        if self.request.user.is_authenticated:
            context['user_rating'] = self.object.get_user_rating(self.request.user)
        else:
            context['user_rating'] = None
            
        return context


class RateRecipeView(LoginRequiredMixin, CreateView):
    """Handle recipe rating (create or update)."""
    
    model = Rating
    fields = ['stars']
    
    def dispatch(self, request, *args, **kwargs):
        self.recipe = get_object_or_404(Recipe, pk=kwargs['recipe_pk'])
        
        # Prevent rating own recipe
        if self.recipe.author == request.user:
            messages.error(request, "You cannot rate your own recipe.")
            return redirect('recipe_detail', pk=self.recipe.pk)
        
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        # Check if user already rated - update instead of create
        rating, created = Rating.objects.update_or_create(
            recipe=self.recipe,
            user=self.request.user,
            defaults={'stars': form.cleaned_data['stars']}
        )
        
        if created:
            messages.success(self.request, "Thank you for rating this recipe!")
        else:
            messages.success(self.request, "Your rating has been updated.")
        
        return redirect('recipe_detail', pk=self.recipe.pk)