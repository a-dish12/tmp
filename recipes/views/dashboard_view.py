from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from recipes.models import Recipe


class DashboardView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'dashboard.html'
    context_object_name = 'recipes'
    
    def get_queryset(self):
        min_time = self.request.GET.get('min_time', 0)
        max_time = self.request.GET.get('max_time', 1000)
        return Recipe.objects.exclude(author=self.request.user).filter(time__range=[min_time, max_time])