### Helper function and classes go here.
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def visible_recipes_for(user):
    """
    Returns a queryset of Recipe objects visible to `user`, based on account-level privacy.

    Rules:
    - Anonymous users: only recipes whose author is public (is_private=False)
    - Authenticated users: own recipes OR public authors OR private authors they follow (accepted follows)
    """
    from recipes.models.recipes import Recipe
    from recipes.models.follow import Follow

    # Anonymous user
    if not user or not user.is_authenticated:
        return Recipe.objects.filter(author__is_private=False).distinct()

    following_ids = Follow.objects.filter(
        follower = user
    ).values_list("following_id", flat=True)

    return Recipe.objects.filter(
        Q(author=user) | # own recipes
        Q(author__is_private=False) | # public accounts' recipes
        Q(author_id__in=following_ids) # private accounts' recipes you follow
    ).distinct()