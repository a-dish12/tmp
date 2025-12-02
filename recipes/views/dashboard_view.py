from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from recipes.models import Recipe, Follow
from django.urls import reverse
from django.db.models import Avg, Count, Q
from recipes.models import Recipe, Follow, User


class DashboardView(LoginRequiredMixin, ListView):
    model = Recipe
    using = Follow
    template_name = "dashboard.html"
    context_object_name = "recipes"

    MEAL_TYPE_FILTERS = (
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
        ("snack", "Snack"),
        ("dessert", "Dessert"),
    )

    TIME_FILTERS = (
        {"key": "under_20", "label": "Up to 20 minutes", "min": 0, "max": 20},
        {"key": "under_30", "label": "Up to 30 minutes", "min": 0, "max": 30},
        {"key": "under_45", "label": "Up to 45 minutes", "min": 0, "max": 45},
        {"key": "under_60", "label": "Up to 60 minutes", "min": 0, "max": 60},
        {"key": "over_90", "label": "90 minutes and above", "min": 90, "max": 1000},
    )
    using = Follow
    template_name = 'dashboard.html'
    context_object_name = 'recipes'

    DIET_FILTERS = (
        ("vegan", "Vegan"),
        ("veg", "Vegetarian"),
        ("non_veg", "Non-Vegetarian"),
    )


    def get_queryset(self):
        queryset = Recipe.objects.exclude(author=self.request.user).annotate(
            avg_rating=Avg('ratings__stars'),
            rating_count=Count('ratings')
        )
        
        queryset = self.filter_by_meal_types(queryset)
        queryset = self.filter_by_time(queryset)
        queryset = self.search_feature(queryset)
        queryset = self.following_only(queryset)
        queryset = self.following_only(queryset)
        queryset = self.filter_by_diet(queryset)

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        selected_meal_types = self.get_selected_meal_types()
        selected_time_filter = self.request.GET.get("time_filter", "")
        search_term = self.request.GET.get("search", "")
        selected_diet = self.get_selected_diet()

        context["meal_type_filters"] = self.MEAL_TYPE_FILTERS
        context["time_filters"] = self.TIME_FILTERS
        context["diet_filters"] = self.DIET_FILTERS

        context["selected_meal_types"] = selected_meal_types
        context["selected_time_filter"] = selected_time_filter
        context["search_term"] = search_term
        context["selected_diet"] = selected_diet
        context["selected_meal_type"] = selected_meal_types[0] if selected_meal_types else ""

        context["has_active_filters"] = bool(
            selected_meal_types or selected_time_filter or search_term or selected_diet
        )

        context["selected_meal_type"] = self.request.GET.get("meal_type", "")
        context["following_page"] = self.request.path == reverse('following_dashboard')
        context["following_page"] = self.request.path == reverse('following_dashboard')
        if self.request.path == self.request.get_full_path():
            context["add_on"] = '?'
        else:
            context["add_on"] = '&'
        return context


    def get_selected_meal_types(self):
        """
        Support both:
        - new style: ?meal_types=breakfast&meal_types=lunch
        - legacy: ?meal_type=breakfast
        """
        meal_types = [
            meal.strip().lower()
            for meal in self.request.GET.getlist("meal_types")
            if meal
        ]

        single_meal_type = self.request.GET.get("meal_type")
        if single_meal_type:
            meal_types.append(single_meal_type.strip().lower())

        # Deduplicate while preserving order
        seen = set()
        unique_meal_types = []
        for meal_type in meal_types:
            if meal_type not in seen:
                unique_meal_types.append(meal_type)
                seen.add(meal_type)

        return unique_meal_types
    
    def get_selected_diet(self):
        """
        Read ?diet= from the query string and validate it.
        """
        diet = self.request.GET.get("diet", "").strip().lower()
        valid_codes = {code for code, _ in self.DIET_FILTERS}
        if diet in valid_codes:
            return diet
        return ""


    def filter_by_meal_types(self, queryset):
        meal_types = self.get_selected_meal_types()
        if meal_types:
            queryset = queryset.filter(meal_type__in=meal_types)
        return queryset
        
    def filter_by_diet(self, queryset):
        """
        Filter recipes by diet type using Recipe.get_diet_type(),
        which inspects the ingredients text.
        """
        selected_diet = self.get_selected_diet()
        if not selected_diet:
            return queryset

        filtered = []
        for recipe in queryset:
            if recipe.get_diet_type() == selected_diet:
                filtered.append(recipe)
        return filtered


    def get_time_window(self):
        """
        Use named time_filter if present, otherwise fall back to min_time/max_time.
        """
        time_filter_key = self.request.GET.get("time_filter")

        for time_filter in self.TIME_FILTERS:
            if time_filter["key"] == time_filter_key:
                return time_filter["min"], time_filter["max"]

        # Fallback to legacy behaviour (?min_time= / ?max_time=)
        min_time = self.parse_int(self.request.GET.get("min_time"), 0)
        max_time = self.parse_int(self.request.GET.get("max_time"), 1000)
        return min_time, max_time

    def parse_int(self, value, default):
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def filter_by_time(self, queryset):
        min_time, max_time = self.get_time_window()
        return queryset.filter(time__range=[min_time, max_time])

    def search_feature(self, queryset):
        # Get the search term from the input URL
        search_term = self.request.GET.get('search')

        #If user typed something in the search bar
        if search_term:
            queryset = queryset.filter(title__icontains=search_term)
        return queryset

    def following_only(self, queryset):
        following_page = self.request.path == reverse('following_dashboard')
        recipe_set = Follow.objects.exclude(follower=self.request.user)

        #Remove recipes from people you don't follow
        if following_page:
            for r in recipe_set.values_list('following'):
                queryset = queryset.exclude(author=r)

        return queryset

    def following_only(self, queryset):
        following_page = self.request.path == reverse('following_dashboard')
        recipe_set = Follow.objects.exclude(follower=self.request.user)

        #Remove recipes from people you don't follow
        if following_page:
            for r in recipe_set.values_list('following'):
                queryset = queryset.exclude(author=r)

        return queryset

    def following_only(self, queryset):
        following_page = self.request.GET.get('following', False)
        recipe_set = Follow.objects.exclude(follower=self.request.user)

        #Remove recipes from people you don't follow
        if following_page:
            for r in recipe_set.values_list('following'):
                queryset = queryset.exclude(author=r)

        return queryset