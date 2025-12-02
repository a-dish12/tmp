from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from recipes.models import Recipe, Follow, User


class DashboardView(LoginRequiredMixin, ListView):
    model = Recipe
    using = Follow
    template_name = 'dashboard.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        queryset = Recipe.objects.exclude(author=self.request.user)
        queryset = self.filter_by_meal_type(queryset)
        queryset = self.filter_by_time(queryset)
        queryset = self.search_feature(queryset)
        queryset = self.following_only(queryset)

        return queryset
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_meal_type"] = self.request.GET.get("meal_type", "")
        context["following_page"] = self.request.GET.get('following', False)
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

    def following_only(self, queryset):
        following_page = self.request.GET.get('following', False)
        recipe_set = Follow.objects.exclude(follower=self.request.user)

        #Remove recipes from people you don't follow
        if following_page:
            for r in recipe_set.values_list('following'):
                queryset = queryset.exclude(author=r)

        return queryset