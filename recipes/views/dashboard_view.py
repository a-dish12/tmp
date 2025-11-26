from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from recipes.models import Recipe


class DashboardView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'dashboard.html'
    context_object_name = 'recipes'
    
    def get_queryset(self):
        queryset= Recipe.objects.exclude(author=self.request.user)

        # Get the search term from the input URL
        search_term = self.request.GET.get('search')

        #If user typed something in the search bar
        if search_term:
            queryset = queryset.filter(title__icontains=search_term)
        
        return queryset
    
    