from django.shortcuts import render, redirect
from recipes.views.dashboard_view import DashboardView
from django.urls import reverse

def surprise_quiz_view(request):
    """Display the surprise me form with filters"""
    # Get filter options from DashboardView
    context = {
        "meal_type_filters": DashboardView.MEAL_TYPE_FILTERS,
        "time_filters": DashboardView.TIME_FILTERS,
        "diet_filters": DashboardView.DIET_FILTERS,
    }
    
    return render(request, "surprise-quiz.html", context)

__all__ = ['surprise_quiz_view']