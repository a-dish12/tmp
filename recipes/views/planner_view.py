from datetime import date as date_cls, timedelta
from datetime import date
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone

from recipes.helpers import visible_recipes_for
from recipes.models.planned_day import PlannedDay
from recipes.models.planned_meal import PlannedMeal
from recipes.models import Recipe
from recipes.forms.planned_meal_form import PlannedMealForm

# Export all planner view functions from this module
__all__ = [
    'planner_calendar',
    'planner_events',
    'planner_day',
    'add_to_planner',
    'remove_from_planner',
    'planner_range',
    'ingredients_list'
]


@login_required
def planner_calendar(request):
    """
    Renders the planner page that contains the FullCalendar UI
    (month/week/day/list views handled on the client side).
    """
    return render(request, "planner_range.html")


@login_required
def planner_events(request):
    """
    Returns planned meals as FullCalendar events (JSON).

    FullCalendar sends "start" and "end" as query parameters.
    This endpoint returns a list of event objects expected by FullCalendar.
    """

    # FullCalendar range filters
    start_str = request.GET.get("start")
    end_str = request.GET.get("end")

    # Convert query params into date objects (or None if missing)
    start = parse_date(start_str) if start_str else None
    end = parse_date(end_str) if end_str else None

    # Fetch all planned meals for the current user (include related day/recipe to reduce queries)
    query_set = PlannedMeal.objects.filter(
        planned_day__user=request.user
    ).select_related(
        "planned_day", "recipe"
    )

    # Apply optional date range filtering (start inclusive, end exclusive)
    if start:
        query_set = query_set.filter(planned_day__date__gte=start)
    if end:
        query_set = query_set.filter(planned_day__date__lt=end)

    # Convert planned meals into FullCalendar event dictionaries
    events = []
    for planned_meal in query_set:
        day = planned_meal.planned_day.date.isoformat()

        events.append({
            "title": f"{planned_meal.meal_type.title()}: {planned_meal.recipe.title}",
            "start": planned_meal.planned_day.date.isoformat(),
            "allDay": True,
            # Clicking the event should take the user to the planner day view
            "url": reverse("planner_day", args=[day])
        })

    return JsonResponse(events, safe=False)


@login_required
def planner_day(request, date):
    """
    Displays the planner for a single day, and allows adding a meal
    (breakfast/lunch/dinner/snack) for the given YYYY-MM-DD date.
    """

    # Parse date from URL
    day_date = parse_date(date)
    if not day_date:
        raise Http404("Invalid date format. Use YYYY-MM-DD")

    # Handle meal-add submission
    if request.method == "POST":
        form = PlannedMealForm(request.POST, user=request.user)
        if form.is_valid():
            meal_type = form.cleaned_data["meal_type"]
            recipe = form.cleaned_data["recipe"]

            # Enforce that the selected recipe is visible to the current user
            if not visible_recipes_for(request.user).filter(pk=recipe.pk).exists():
                raise Http404("Recipe not visible.")

            # Ensure there is a PlannedDay entry for this user and date
            planned_day, _ = PlannedDay.objects.get_or_create(
                user=request.user,
                date=day_date
            )

            # Create the planned meal entry (or do nothing if it already exists)
            PlannedMeal.objects.get_or_create(
                planned_day=planned_day,
                meal_type=meal_type,
                recipe=recipe
            )

            # Optional redirect target (useful when coming from another page)
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)

            return redirect("planner_day", date=day_date.isoformat())

    else:
        # GET request: initialise a blank form
        form = PlannedMealForm(user=request.user)

    # Fetch the day's PlannedDay object if it exists
    planned_day = PlannedDay.objects.filter(user=request.user, date=day_date).first()

    # Fetch all meals for this planned day (ordered by meal type for consistent display)
    meals = []
    if planned_day:
        meals = planned_day.meals.select_related("recipe").all().order_by("meal_type")

    context = {
        "planned_day": planned_day,   # can be None if the user has not planned anything yet
        "day_date": day_date,
        "meals": meals,
        "form": form,
    }
    return render(request, "day.html", context)


@login_required
def add_to_planner(request, recipe_pk):
    """
    Adds a recipe to the planner from the recipe detail page.

    Expects a POST request containing:
      - date (YYYY-MM-DD)
      - meal_type (e.g. breakfast/lunch/dinner/snack)
    """

    recipe = get_object_or_404(Recipe, pk=recipe_pk)

    # Ensure the recipe is visible to the current user
    if not visible_recipes_for(request.user).filter(pk=recipe.pk).exists():
        raise Http404("Recipe not visible.")

    if request.method == "POST":
        date_str = request.POST.get("date")
        meal_type = request.POST.get("meal_type")

        # Validate required fields
        if not date_str or not meal_type:
            messages.error(request, "Please select both a date and meal type.")
            return redirect("recipe_detail", pk=recipe_pk)

        # Parse and validate date
        day_date = parse_date(date_str)
        if not day_date:
            messages.error(request, "Invalid date format.")
            return redirect("recipe_detail", pk=recipe_pk)

        # Create (or fetch) PlannedDay for this user and date
        planned_day, created = PlannedDay.objects.get_or_create(
            user=request.user,
            date=day_date
        )

        # Create (or fetch) the planned meal record
        meal, created = PlannedMeal.objects.get_or_create(
            planned_day=planned_day,
            meal_type=meal_type,
            recipe=recipe
        )

        # Provide feedback message depending on whether the record was newly created
        if created:
            messages.success(
                request,
                f"Added '{recipe.title}' to {meal_type} on {day_date.strftime('%B %d, %Y')}."
            )
        else:
            messages.info(
                request,
                f"This recipe is already planned for {meal_type} on {day_date.strftime('%B %d, %Y')}."
            )

        return redirect("recipe_detail", pk=recipe_pk)

    # Non-POST requests fall back to the recipe detail page
    return redirect("recipe_detail", pk=recipe_pk)


@login_required
def remove_from_planner(request, meal_pk):
    """
    Removes a planned meal from the planner.

    Only the owner of the PlannedDay can remove its meals.
    """

    meal = get_object_or_404(PlannedMeal, pk=meal_pk)

    # Ensure the planned meal belongs to the current user
    if meal.planned_day.user != request.user:
        raise Http404("Meal not found.")

    recipe_title = meal.recipe.title
    meal_type = meal.meal_type
    date_str = meal.planned_day.date.isoformat()

    # Delete the planned meal record
    meal.delete()

    messages.success(request, f"Removed '{recipe_title}' from {meal_type}.")

    # If a next URL is provided, redirect there
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)

    # Default: return to the planner day page
    return redirect("planner_day", date=date_str)


# Supported meal slots displayed on the planner range view
MEAL_SLOTS = ["breakfast", "lunch", "dinner", "snack"]


def daterange(start, end):
    """
    Inclusive date range generator.

    Yields each date from start to end (including both endpoints).
    """
    cur = start
    while cur <= end:
        yield cur
        cur += timedelta(days=1)


@login_required
def planner_range(request):
    """
    Range-based planner view that shows day blocks.

    Default: today -> today+6
    Accepts: ?start=YYYY-MM-DD&end=YYYY-MM-DD

    Note: There is also a POST handler here for the model "add meal" form.
    """

    # Handle modal form submission
    if request.method == "POST":
        date_str = request.POST.get("date")
        meal_type = request.POST.get("meal_type")

        # Recipe selected via datalist input (ID expected)
        recipe_id = request.POST.get("recipe_search")

        # Only proceed if all required fields are present
        if date_str and meal_type and recipe_id:
            day_date = parse_date(date_str)
            if day_date:
                try:
                    recipe = Recipe.objects.get(pk=recipe_id)

                    # Check if recipe is visible to the current user
                    if visible_recipes_for(request.user).filter(pk=recipe.pk).exists():
                        planned_day, _ = PlannedDay.objects.get_or_create(
                            user=request.user,
                            date=day_date
                        )
                        PlannedMeal.objects.get_or_create(
                            planned_day=planned_day,
                            meal_type=meal_type,
                            recipe=recipe
                        )
                        messages.success(request, f"Added {recipe.title} to {meal_type}!")
                except (Recipe.DoesNotExist, ValueError):
                    messages.error(request, "Invalid recipe selected.")

        # Redirect to preserve GET parameters (so the user stays on the same week range)
        start_str = request.POST.get("start") or request.GET.get("start")
        end_str = request.POST.get("end") or request.GET.get("end")
        if start_str and end_str:
            return redirect(f"{reverse('planner_range')}?start={start_str}&end={end_str}")
        return redirect("planner_range")

    # Read range query parameters
    start_str = request.GET.get("start")
    end_str = request.GET.get("end")

    today = timezone.localdate()

    # Default to current week range if no query params were provided
    start = parse_date(start_str) if start_str else today
    end = parse_date(end_str) if end_str else (today + timedelta(days=6))

    # Validate parsed dates
    if not start or not end:
        raise Http404("Invalid date format. Use YYYY-MM-DD")

    # Normalise range ordering
    if start > end:
        start, end = end, start

    # Fetch all meals in the selected range for the current user
    meals_qs = (
        PlannedMeal.objects
        .filter(
            planned_day__user=request.user,
            planned_day__date__gte=start,
            planned_day__date__lte=end,
        )
        .select_related("planned_day", "recipe")
        .order_by("planned_day__date", "meal_type")
    )

    # Group meals by day and slot for easier template rendering
    grouped = {}  # {date: {slot: [PlannedMeal, ...]}}
    for m in meals_qs:
        d = m.planned_day.date
        slot = (m.meal_type or "").lower().strip()

        if d not in grouped:
            grouped[d] = {s: [] for s in MEAL_SLOTS}

        if slot in grouped[d]:
            grouped[d][slot].append(m)

    # Build list of day blocks for the template
    days = []
    for d in daterange(start, end):
        meals_by_slot = grouped.get(d, {s: [] for s in MEAL_SLOTS})

        slots = []
        for slot in MEAL_SLOTS:
            slots.append({
                "name": slot,
                "meals": meals_by_slot.get(slot, []),
            })

        days.append({
            "date": d,
            "slots": slots,
            "is_today": d == today,  # used for highlighting today in the UI
        })

    # Calculate previous and next week dates for navigation
    week_delta = timedelta(days=7)
    prev_week = start - week_delta
    prev_week_end = end - week_delta
    next_week = start + week_delta
    next_week_end = end + week_delta

    # Recipes shown in the modal dropdown (visible recipes only)
    user_recipes = visible_recipes_for(request.user).order_by('title')

    context = {
        "start": start,
        "end": end,
        "days": days,
        "prev_week": prev_week,
        "prev_week_end": prev_week_end,
        "next_week": next_week,
        "next_week_end": next_week_end,
        "user_recipes": user_recipes,
    }

    return render(request, "planner_range.html", context)


@login_required
def ingredients_list(request):
    """
    Generates an ingredient list for the planner over a given date range.

    Accepts:
      - start=YYYY-MM-DD
      - end=YYYY-MM-DD

    If start/end are missing or invalid, defaults to today's date only.
    """

    start = parse_date(request.GET.get("start", ""))
    end = parse_date(request.GET.get("end", ""))

    # Default to today if the range is missing/invalid
    if not start or not end:
        start = end = date.today()

    # Fetch all meals in the given date range
    planned_meals = (
        PlannedMeal.objects
        .filter(planned_day__user=request.user, planned_day__date__range=[start, end])
        .select_related("recipe", "planned_day")
        .order_by("planned_day__date", "meal_type")
    )

    # Collect ingredients line-by-line (no quantity parsing here)
    ingredients_lines = []
    for meal in planned_meals:
        text = (meal.recipe.ingredients or "").strip()
        if not text:
            continue

        for line in text.splitlines():
            line = line.strip()
            if line:
                ingredients_lines.append(line)

    return render(request, "ingredients_list.html", {
        "start": start,
        "end": end,
        "ingredients_lines": ingredients_lines,
    })
