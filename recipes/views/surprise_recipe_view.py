from django.shortcuts import redirect
from recipes.views.dashboard_view import DashboardView

def surprise_recipe_view(request):
    # reusing the dashboard's filtering logic 
    dashboard_view = DashboardView()
    dashboard_view.request = request

    queryset = dashboard_view.get_queryset()
    recipe = queryset.order_by("?").first()

    if recipe is None:
        return redirect("dashboard")
    
    if not queryset.exists():
        return redirect("dashboard")
    
    recipe = queryset.order_by("?").first()
    
    return redirect("recipe_detail", pk=recipe.pk)