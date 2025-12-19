from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from recipes.models import Recipe, Rating
from recipes.models.planned_meal import PlannedMeal
from recipes.forms.comment_form import CommentForm
from recipes.forms.planned_meal_form import PlannedMealForm
from recipes.forms.rating_form import RatingForm
from datetime import date as date_cls


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
            
            # Get planned meals for this recipe
            planned_meals = PlannedMeal.objects.filter(
                recipe=self.object,
                planned_day__user=self.request.user
            ).select_related('planned_day').order_by('planned_day__date')
            context['planned_meals'] = planned_meals
            
            # Today's date for the date picker default
            context['today'] = date_cls.today().isoformat()
            
            # Comment form
            context['comment_form'] = CommentForm()
            
            # Planned meal form for calendar
            context['planned_meal_form'] = PlannedMealForm(user=self.request.user, recipe=self.object)
            
            # Rating form (only if not own recipe)
            if self.request.user != self.object.author:
                initial_data = {'stars': context['user_rating']} if context['user_rating'] else {}
                context['rating_form'] = RatingForm(initial=initial_data)
        else:
            context['user_rating'] = None
            context['planned_meals'] = []
            
        # Get all top-level comments (no parent) with their replies
        top_level_comments = self.object.comments.filter(parent=None).select_related('user').prefetch_related('replies__user', 'replies__replies')
        context['comments'] = top_level_comments
        context['comment_count'] = self.object.comments.count()
            
        return context


class RateRecipeView(LoginRequiredMixin, CreateView):
    """Handle recipe rating (create or update)."""
    
    model = Rating
    form_class = RatingForm
    
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