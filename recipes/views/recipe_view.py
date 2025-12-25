from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from recipes.models import Recipe, Rating
from recipes.models.planned_meal import PlannedMeal
from recipes.forms.comment_form import CommentForm
from recipes.forms.planned_meal_form import PlannedMealForm
from recipes.forms.rating_form import RatingForm
from datetime import date as date_cls
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class RecipeDetailView(DetailView):
    """Display full recipe details with rating."""
    
    model = Recipe
    template_name = 'recipe_detail.html'
    context_object_name = 'recipe'
    
    def get_object(self, queryset=None):
        """Get recipe and track view."""
        obj = super().get_object(queryset)
        
        # Track view for authenticated or anonymous users (exclude staff/superusers)
        if not (self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)):
            user_id = self.request.user.id if self.request.user.is_authenticated else f"anon_{self.request.session.session_key}"
            obj.add_viewer(user_id)
        
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add view metrics
        context['active_viewers'] = self.object.get_active_viewers()
        context['total_views'] = self.object.total_views
        
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
            
        # Get all comments for this recipe, excluding hidden comments
        all_comments = self.object.comments.filter(is_hidden=False).select_related('user').order_by('-created_at')
        comment_count = all_comments.count()

        paginator = Paginator(all_comments, 10)
        page = self.request.GET.get('comments_page')

        try:
            comments_page = paginator.page(page)
        except PageNotAnInteger:
            comments_page = paginator.page(1)
        except EmptyPage:
            comments_page = paginator.page(paginator.num_pages)

        context['comments'] = comments_page.object_list
        context['comments_page_obj'] = comments_page
        context['comments_is_paginated'] = comments_page.has_other_pages()
        context['comment_count'] = comment_count
            
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