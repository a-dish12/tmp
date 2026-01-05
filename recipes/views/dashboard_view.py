from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.urls import reverse
from django.db.models import Avg, Count, F, Q
from recipes.models import Recipe, Follow, User


class DashboardView(LoginRequiredMixin, ListView):
    """main recipe browsing view with filtering, search, sorting and pagination"""
    model = Recipe
    template_name = "dashboard.html"
    context_object_name = "recipes"
    paginate_by = 9

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

    DIET_FILTERS = (
        ("vegan", "Vegan"),
        ("veg", "Vegetarian"),
        ("non_veg", "Non-Vegetarian"),
    )

    SORT_OPTIONS = (
        ("time", "Prep Time (Low to High)"),
        ("popular", "Most Popular"),
        ("trending", "Trending Now"),
        ("most_viewed", "Most Viewed"),
        ("newest", "Newest First"),
    )

    RATING_FILTERS = (
        {"key": "4_plus", "label": "4+ stars", "min": 4.0},
        {"key": "3_plus", "label": "3+ stars", "min": 3.0},
        {"key": "2_plus", "label": "2+ stars", "min": 2.0},
        {"key": "1_plus", "label": "1+ stars", "min": 1.0},
    )

    # ------------------------
    # Queryset logic
    # ------------------------

    def get_queryset(self):
        # exclude own recipes and hidden/reported ones
        queryset = (
            Recipe.objects
            .exclude(author=self.request.user)
            .exclude(is_hidden=True)
            .annotate(
                avg_rating=Avg("ratings__stars"),
                rating_count=Count("ratings"),
            )
        )

        # apply filters in order - diet filter must be last since it returns a list
        queryset = self.filter_by_meal_types(queryset)
        queryset = self.filter_by_time(queryset)
        queryset = self.filter_by_rating(queryset)
        queryset = self.search_feature(queryset)
        queryset = self.following_only(queryset)
        queryset = self.apply_sorting(queryset)
        queryset = self.filter_by_diet(queryset)  # returns list, must be last

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        selected_meal_types = self.get_selected_meal_types()
        selected_time_filter = self.request.GET.get("time_filter", "")
        search_term = self.request.GET.get("search", "")
        selected_diet = self.get_selected_diet()
        selected_sort = self.request.GET.get("sort", "time")
        selected_rating_filter = self.request.GET.get("rating_filter", "")

        context.update({
            "meal_type_filters": self.MEAL_TYPE_FILTERS,
            "time_filters": self.TIME_FILTERS,
            "diet_filters": self.DIET_FILTERS,
            "rating_filters": self.RATING_FILTERS,
            "sort_options": self.SORT_OPTIONS,

            "selected_meal_types": selected_meal_types,
            "selected_meal_type": selected_meal_types[0] if selected_meal_types else "",
            "selected_time_filter": selected_time_filter,
            "search_term": search_term,
            "selected_diet": selected_diet,
            "selected_rating_filter": selected_rating_filter,
            "selected_sort": selected_sort,

            "following_page": self.request.path == reverse("following_dashboard"),

            "has_active_filters": bool(
                selected_meal_types or selected_time_filter or search_term or selected_diet or selected_rating_filter
            ),

            "add_on": "?" if self.request.path == self.request.get_full_path() else "&",
        })

        return context

    def get_selected_meal_types(self):
        """extracts meal type filters from query params and removes duplicates"""
        meal_types = [
            m.strip().lower()
            for m in self.request.GET.getlist("meal_types")
            if m
        ]

        single_meal_type = self.request.GET.get("meal_type")
        if single_meal_type:
            meal_types.append(single_meal_type.strip().lower())

        # deduplicate while preserving order
        seen = set()
        unique = []
        for m in meal_types:
            if m not in seen:
                unique.append(m)
                seen.add(m)

        return unique

    def get_selected_diet(self):
        diet = self.request.GET.get("diet", "").strip().lower()
        valid = {code for code, _ in self.DIET_FILTERS}
        return diet if diet in valid else ""

    def get_time_window(self):
        time_filter_key = self.request.GET.get("time_filter")

        for tf in self.TIME_FILTERS:
            if tf["key"] == time_filter_key:
                return tf["min"], tf["max"]

        min_time = self.parse_int(self.request.GET.get("min_time"), 0)
        max_time = self.parse_int(self.request.GET.get("max_time"), 1000)
        return min_time, max_time

    def parse_int(self, value, default):
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def filter_by_meal_types(self, queryset):
        meal_types = self.get_selected_meal_types()
        if meal_types:
            queryset = queryset.filter(meal_type__in=meal_types)
        return queryset

    def filter_by_time(self, queryset):
        min_time, max_time = self.get_time_window()
        return queryset.filter(time__range=(min_time, max_time))
    
    def filter_by_diet(self, queryset):
        """filters by diet type - returns list so must be applied last"""
        selected_diet = self.get_selected_diet()
        if not selected_diet:
            return queryset

        return [
            recipe for recipe in queryset
            if recipe.get_diet_type() == selected_diet
        ]


    def filter_by_rating(self, queryset):
        rating_filter_key = self.request.GET.get("rating_filter")
        
        if not rating_filter_key:
            return queryset
        
        for rf in self.RATING_FILTERS:
            if rf["key"] == rating_filter_key:
                min_rating = rf["min"]
                return queryset.filter(avg_rating__gte=min_rating)
        
        return queryset

    def search_feature(self, queryset):
        search_term = self.request.GET.get("search")
        if search_term:
            queryset = queryset.filter(
                Q(description__icontains=search_term) |
                Q(ingredients__icontains=search_term) |
                Q(title__icontains=search_term) |
                Q(meal_type__icontains=search_term))

        return queryset

    def following_only(self, queryset):
        """filters recipes based on following relationships and privacy settings"""
        following_page = self.request.path == reverse('following_dashboard')
        followed_users = Follow.objects.filter(follower=self.request.user).values_list('following')
        followed_recipes = queryset.filter(author__in=followed_users)

        if following_page:
            queryset = followed_recipes
        else:
            # show public recipes plus recipes from followed users
            public_users = User.objects.filter(is_private=False)
            queryset = queryset.filter(author__in=public_users)

            queryset: QuerySet = (queryset|followed_recipes).distinct()

        return queryset
    
    def apply_sorting(self, queryset):
        """applies sorting - trending returns list so needs special handling"""
        sort_by = self.request.GET.get("sort", "time")
        
        if sort_by == "popular":
            # popularity = avg_rating * rating_count
            queryset = queryset.annotate(
                popularity_score=F('avg_rating') * F('rating_count')
            ).order_by('-popularity_score', '-avg_rating')
        elif sort_by == "trending":
            # Sort by recipes with most active viewers
            recipes_list = list(queryset)
            recipes_list.sort(key=lambda r: r.get_active_viewers(), reverse=True)
            # Return as list (already evaluated)
            return recipes_list
        elif sort_by == "most_viewed":
            # Sort by total views descending
            queryset = queryset.order_by('-total_views')
        elif sort_by == "newest":
            # Sort by creation date descending
            queryset = queryset.order_by('-created_at')
        else:  # Default: "time"
            # Sort by preparation time ascending
            queryset = queryset.order_by('time')
        
        return queryset