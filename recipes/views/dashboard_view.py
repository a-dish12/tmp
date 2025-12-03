from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from recipes.models import Recipe
from django.db.models import Avg,Count



class DashboardView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'dashboard.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        queryset = Recipe.objects.exclude(author=self.request.user).annotate(
            avg_rating=Avg('ratings__stars'),
            rating_count=Count('ratings')
        )
        queryset = self.filter_by_meal_type(queryset)
        queryset = self.filter_by_time(queryset)
        queryset = self.search_feature(queryset)

        return queryset
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_meal_type"] = self.request.GET.get("meal_type", "")
        return context

    def filter_by_meal_type(self, queryset):
        meal_type = self.request.GET.get('meal_type', '').strip().lower()

        if meal_type:
            queryset = queryset.filter(meal_type__iexact=meal_type)

        return queryset

    def filter_by_time(self, queryset):
        min_time = self.request.GET.get('min_time', 0)
        max_time = self.request.GET.get('max_time', 1000)
        return queryset.filter(time__range=[min_time, max_time])

    def search_feature(self, queryset):
        # Get the search term from the input URL
        search_term = self.request.GET.get('search')

        #If user typed something in the search bar
        if search_term:
            queryset = queryset.filter(title__icontains=search_term)

        return queryset