from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from recipes.models import Recipe, Comment
from recipes.forms.comment_form import CommentForm, ReplyForm


@login_required
def add_comment(request, recipe_pk):
    """Add a new comment to a recipe."""
    recipe = get_object_or_404(Recipe, pk=recipe_pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.user = request.user
            comment.save()
            messages.success(request, "Comment added successfully!")
        else:
            messages.error(request, "Failed to add comment. Please try again.")
    
    return redirect('recipe_detail', pk=recipe_pk)


@login_required
def add_reply(request, comment_pk):
    """Add a reply to an existing comment."""
    parent_comment = get_object_or_404(Comment, pk=comment_pk)
    
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.recipe = parent_comment.recipe
            reply.user = request.user
            reply.parent = parent_comment
            reply.save()
            messages.success(request, "Reply added successfully!")
        else:
            messages.error(request, "Failed to add reply. Please try again.")
    
    return redirect('recipe_detail', pk=parent_comment.recipe.pk)


@login_required
def delete_comment(request, comment_pk):
    """Delete a comment (only by the comment author)."""
    comment = get_object_or_404(Comment, pk=comment_pk)
    
    # Check if user is the comment author
    if comment.user != request.user:
        messages.error(request, "You can only delete your own comments.")
        return redirect('recipe_detail', pk=comment.recipe.pk)
    
    recipe_pk = comment.recipe.pk
    comment.delete()
    messages.success(request, "Comment deleted successfully!")
    
    return redirect('recipe_detail', pk=recipe_pk)
