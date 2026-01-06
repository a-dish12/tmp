from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from recipes.models import Recipe, Comment, Notification
from recipes.forms.comment_form import CommentForm


@login_required
def add_comment(request, recipe_pk):
    recipe = get_object_or_404(Recipe, pk=recipe_pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.user = request.user
            comment.save()
            
            # Send notification to recipe author (unless commenting on own recipe)
            if recipe.author != request.user:
                Notification.create_comment_notification(request.user, recipe)
            
            messages.success(request, "Comment added successfully!")
        else:
            messages.error(request, "Failed to add comment. Please try again.")
    
    return redirect('recipe_detail', pk=recipe_pk)


@login_required
def delete_comment(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    recipe_pk = comment.recipe.pk

    if comment.user == request.user or request.user.is_staff:
        comment.delete()
        messages.success(request, "Comment deleted successfully!")
    else:
        messages.error(request, "You don't have permission to delete this comment.")

    return redirect('recipe_detail', pk=recipe_pk)

