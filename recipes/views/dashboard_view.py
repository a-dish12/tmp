from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from recipes.models import Recipe


class DashboardView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'dashboard.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        queryset = Recipe.objects.exclude(author=self.request.user)
        meal_type = self.request.GET.get('meal_type', '').strip().lower()

        if meal_type:
            queryset = queryset.filter(meal_type__iexact=meal_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_meal_type"] = self.request.GET.get("meal_type", "")
        return context
