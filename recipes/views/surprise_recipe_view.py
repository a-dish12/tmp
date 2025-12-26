from django.shortcuts import render, redirect
from django.contrib import messages
from recipes.views.dashboard_view import DashboardView
import random

def surprise_recipe_view(request):
    """Get a random recipe based on selected filters"""
    try:
        # Reusing the dashboard's filtering logic 
        dashboard_view = DashboardView()
        dashboard_view.request = request
        queryset = dashboard_view.get_queryset()
        
        # Handle both QuerySet and list types
        if queryset is None:
            recipe_list = []
        elif hasattr(queryset, 'count'):
            # It's a QuerySet
            recipe_list = list(queryset)
        else:
            # It's already a list
            recipe_list = queryset
        
        # Check if we have any recipes
        if not recipe_list:
            messages.warning(request, "No recipes found matching your criteria. Please try different filters.")
            # Get filter options to re-render the form
            context = {
                "meal_type_filters": DashboardView.MEAL_TYPE_FILTERS,
                "time_filters": DashboardView.TIME_FILTERS,
                "diet_filters": DashboardView.DIET_FILTERS,
            }
            return render(request, "surprise-quiz.html", context)
        
        # Get random recipe
        recipe = random.choice(recipe_list)
        
        # Make sure recipe has pk
        if not recipe or not hasattr(recipe, 'pk'):
            messages.error(request, "Something went wrong. Please try again.")
            context = {
                "meal_type_filters": DashboardView.MEAL_TYPE_FILTERS,
                "time_filters": DashboardView.TIME_FILTERS,
                "diet_filters": DashboardView.DIET_FILTERS,
            }
            return render(request, "surprise-quiz.html", context)
        
        return redirect("recipe_detail", pk=recipe.pk)
        
    except Exception as e:
        # If anything goes wrong, show error and stay on page
        print(f"Error in surprise_recipe_view: {e}")
        messages.error(request, "Something went wrong. Please try again.")
        context = {
            "meal_type_filters": DashboardView.MEAL_TYPE_FILTERS,
            "time_filters": DashboardView.TIME_FILTERS,
            "diet_filters": DashboardView.DIET_FILTERS,
        }
        return render(request, "surprise-quiz.html", context)

__all__ = ['surprise_recipe_view']