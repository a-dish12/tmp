from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.urls import reverse
from django.db.models import Avg, Count, F
from recipes.models import Recipe, Follow
from django.db.models import Q


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

    # ------------------------
    # Queryset logic
    # ------------------------

    def get_queryset(self):
        queryset = (
            Recipe.objects
            .exclude(author=self.request.user)
            .exclude(is_hidden=True)  # Hide reported/moderated recipes
            .annotate(
                avg_rating=Avg("ratings__stars"),
                rating_count=Count("ratings"),
            )
        )

        queryset = self.filter_by_meal_types(queryset)
        queryset = self.filter_by_time(queryset)
        queryset = self.search_feature(queryset)
        queryset = self.following_only(queryset)
        queryset = self.filter_by_diet(queryset)
        queryset = self.apply_sorting(queryset)

        return queryset

    # ------------------------
    # Context
    # ------------------------

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        selected_meal_types = self.get_selected_meal_types()
        selected_time_filter = self.request.GET.get("time_filter", "")
        search_term = self.request.GET.get("search", "")
        selected_diet = self.get_selected_diet()
        selected_sort = self.request.GET.get("sort", "time")

        context.update({
            "meal_type_filters": self.MEAL_TYPE_FILTERS,
            "time_filters": self.TIME_FILTERS,
            "diet_filters": self.DIET_FILTERS,
            "sort_options": self.SORT_OPTIONS,

            "selected_meal_types": selected_meal_types,
            "selected_meal_type": selected_meal_types[0] if selected_meal_types else "",
            "selected_time_filter": selected_time_filter,
            "search_term": search_term,
            "selected_diet": selected_diet,
            "selected_sort": selected_sort,

            "following_page": self.request.path == reverse("following_dashboard"),

            "has_active_filters": bool(
                selected_meal_types or selected_time_filter or search_term or selected_diet or (selected_sort != "time")
            ),

            "add_on": "?" if self.request.path == self.request.get_full_path() else "&",
        })

        return context

    # ------------------------
    # Helpers
    # ------------------------

    def get_selected_meal_types(self):
        """
        Supports:
        - ?meal_types=breakfast&meal_types=lunch
        - ?meal_type=breakfast (legacy)
        """
        meal_types = [
            m.strip().lower()
            for m in self.request.GET.getlist("meal_types")
            if m
        ]

        single_meal_type = self.request.GET.get("meal_type")
        if single_meal_type:
            meal_types.append(single_meal_type.strip().lower())

        # Deduplicate while preserving order
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

    # ------------------------
    # Filters
    # ------------------------

    def filter_by_meal_types(self, queryset):
        meal_types = self.get_selected_meal_types()
        if meal_types:
            queryset = queryset.filter(meal_type__in=meal_types)
        return queryset

    def filter_by_time(self, queryset):
        min_time, max_time = self.get_time_window()
        return queryset.filter(time__range=(min_time, max_time))

    def search_feature(self, queryset):
        search_term = self.request.GET.get("search")
        if search_term:
            queryset = queryset.filter(
                Q(description__icontains=search_term) |
                Q(ingredients__icontains=search_term) |
                Q(title__icontains=search_term) |
                Q(meal_type__icontains=search_term))

        return queryset

    def filter_by_diet(self, queryset):
        selected_diet = self.get_selected_diet()
        if not selected_diet:
            return queryset


    def following_only(self, queryset):
        following_page = self.request.path == reverse('following_dashboard')
        not_following_set = Follow.objects.filter(follower=self.request.user)

        #Remove recipes from people you don't follow
        if following_page:
            temp_set = queryset
            for nf in not_following_set.values_list('following'):
                temp_set = temp_set.exclude(author=nf)
            for f in temp_set.values_list('author'):
                queryset = queryset.exclude(author=f)

        return queryset
    
    def apply_sorting(self, queryset):
        """Apply sorting based on user selection."""
        sort_by = self.request.GET.get("sort", "time")
        
        if sort_by == "popular":
            # Sort by rating score (avg_rating * rating_count) descending
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
