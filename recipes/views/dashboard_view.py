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

        return self.filter_by_time(Recipe.objects.exclude(author=self.request.user))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_meal_type"] = self.request.GET.get("meal_type", "")
        return context


    def filter_by_time(self, queryset):
        min_time = self.request.GET.get('min_time', 0)
        max_time = self.request.GET.get('max_time', 1000)
        return queryset.filter(time__range=[min_time, max_time])