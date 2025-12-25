from datetime import date as date_cls
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date
from django.urls import reverse
from django.contrib import messages

from recipes.helpers import visible_recipes_for
from recipes.models.planned_day import PlannedDay
from recipes.models.planned_meal import PlannedMeal
from recipes.models import Recipe
from recipes.forms.planned_meal_form import PlannedMealForm


@login_required
def planner_calendar(request):
    """
    Renders the FullCalendar page (month/week/day/list all on one page).
    """
    return render(request, "planner_range.html")

@login_required
def planner_events(request):
    """
    Returns planned meals as FullCalendar events (JSON).
    FullCalendar sends start/end as query params.
    """

    start_str = request.GET.get("start")
    end_str = request.GET.get("end")

    start  = parse_date(start_str) if start_str else None
    end  = parse_date(end_str) if end_str else None

    query_set = PlannedMeal.objects.filter(planned_day__user=request.user).select_related(
        "planned_day", "recipe"
    )

    if start:
        query_set = query_set.filter(planned_day__date__gte = start)
    if end:
        query_set = query_set.filter(planned_day__date__lt=end)

    events = []
    for planned_meal in query_set:
        day = planned_meal.planned_day.date.isoformat()

        events.append({
            "title": f"{planned_meal.meal_type.title()}: {planned_meal.recipe.title}",
            "start": planned_meal.planned_day.date.isoformat(),
            "allDay": True,
            "url": reverse("planner_day", args=[day])
        })

    return JsonResponse(events, safe = False)

@login_required
def planner_day(request, date):
    """
    Day page: shows planned meals + allows adding a meal (breakfast/lunch/dinner/snack)
    for the given YYYY-MM-DD date.
    """
    day_date = parse_date(date)
    if not day_date:
        raise Http404("Invalid date format. Use YYYY-MM-DD")
    if request.method == "POST":
        form = PlannedMealForm(request.POST, user=request.user)
        if form.is_valid():
            meal_type = form.cleaned_data["meal_type"]
            recipe = form.cleaned_data["recipe"]

            if not visible_recipes_for(request.user).filter(pk=recipe.pk).exists():
                raise Http404("Recipe not visible.")

            planned_day, _ = PlannedDay.objects.get_or_create(
                user=request.user,
                date=day_date
            )
            PlannedMeal.objects.get_or_create(
                planned_day=planned_day,
                meal_type=meal_type,
                recipe=recipe
            )
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)
            
            return redirect("planner_day", date=day_date.isoformat())

    else:
        form = PlannedMealForm(user=request.user)

    planned_day = PlannedDay.objects.filter(user=request.user, date=day_date).first()

    meals = []
    if planned_day:
        meals = planned_day.meals.select_related("recipe").all().order_by("meal_type")

    context = {
        "planned_day": planned_day,   # can be None now
        "day_date": day_date,
        "meals": meals,
        "form": form,
    }
    return render(request, "day.html", context)

@login_required
def add_to_planner(request, recipe_pk):
    """
    Add a recipe to the planner from the recipe detail page.
    """
    recipe = get_object_or_404(Recipe, pk=recipe_pk)
    
    # Check if recipe is visible to user
    if not visible_recipes_for(request.user).filter(pk=recipe.pk).exists():
        raise Http404("Recipe not visible.")
    
    if request.method == "POST":
        date_str = request.POST.get("date")
        meal_type = request.POST.get("meal_type")
        
        if not date_str or not meal_type:
            messages.error(request, "Please select both a date and meal type.")
            return redirect("recipe_detail", pk=recipe_pk)
        
        day_date = parse_date(date_str)
        if not day_date:
            messages.error(request, "Invalid date format.")
            return redirect("recipe_detail", pk=recipe_pk)
        
        # Get or create the planned day
        planned_day, created = PlannedDay.objects.get_or_create(
            user=request.user,
            date=day_date
        )
        
        # Add the meal (or get if already exists)
        meal, created = PlannedMeal.objects.get_or_create(
            planned_day=planned_day,
            meal_type=meal_type,
            recipe=recipe
        )
        
        if created:
            messages.success(request, f"Added '{recipe.title}' to {meal_type} on {day_date.strftime('%B %d, %Y')}.")
        else:
            messages.info(request, f"This recipe is already planned for {meal_type} on {day_date.strftime('%B %d, %Y')}.")
        
        return redirect("recipe_detail", pk=recipe_pk)
    
    return redirect("recipe_detail", pk=recipe_pk)

@login_required
def remove_from_planner(request, meal_pk):
    """
    Remove a planned meal from the planner.
    """
    meal = get_object_or_404(PlannedMeal, pk=meal_pk)
    
    # Ensure the meal belongs to the current user
    if meal.planned_day.user != request.user:
        raise Http404("Meal not found.")
    
    recipe_title = meal.recipe.title
    meal_type = meal.meal_type
    date_str = meal.planned_day.date.isoformat()
    
    meal.delete()
    
    messages.success(request, f"Removed '{recipe_title}' from {meal_type}.")
    
    # Check where to redirect based on referer
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    
    # Default to planner day view
    return redirect("planner_day", date=date_str)

from datetime import timedelta
from django.utils import timezone

MEAL_SLOTS = ["breakfast", "lunch", "dinner", "snack"]

def daterange(start, end):
    """Inclusive date range generator."""
    cur = start
    while cur <= end:
        yield cur
        cur += timedelta(days=1)

@login_required
def planner_range(request):
    """
    Range-based planner view (day blocks).
    Default: today -> today+6
    Accepts: ?start=YYYY-MM-DD&end=YYYY-MM-DD
    """
    start_str = request.GET.get("start")
    end_str = request.GET.get("end")

    today = timezone.localdate()

    start = parse_date(start_str) if start_str else today
    end = parse_date(end_str) if end_str else (today + timedelta(days=6))

    if not start or not end:
        raise Http404("Invalid date format. Use YYYY-MM-DD")

    if start > end:
        start, end = end, start

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

    grouped = {}  # {date: {slot: [PlannedMeal,...]}}
    for m in meals_qs:
        d = m.planned_day.date
        slot = (m.meal_type or "").lower().strip()

        if d not in grouped:
            grouped[d] = {s: [] for s in MEAL_SLOTS}

        if slot in grouped[d]:
            grouped[d][slot].append(m)

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
        })

    context = {
        "start": start,
        "end": end,
        "days": days,
    }

    return render(request, "planner_range.html", context)
