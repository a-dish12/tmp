"""Views for reporting content."""
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from recipes.models import Recipe, Comment, Report, Notification
from recipes.forms.report_form import ReportForm


@login_required
def report_recipe(request, recipe_pk):
    """Report a recipe for inappropriate content."""
    recipe = get_object_or_404(Recipe, pk=recipe_pk)
    
    # Prevent staff/superusers from reporting
    if request.user.is_staff or request.user.is_superuser:
        messages.error(request, "Staff members cannot submit reports.")
        return redirect('recipe_detail', pk=recipe_pk)
    
    # Prevent reporting own content
    if recipe.author == request.user:
        messages.error(request, "You cannot report your own recipe.")
        return redirect('recipe_detail', pk=recipe_pk)
    
    # Check if user already reported this recipe
    content_type = ContentType.objects.get_for_model(Recipe)
    existing_report = Report.objects.filter(
        reported_by=request.user,
        content_type=content_type,
        object_id=recipe_pk
    ).exists()
    
    if existing_report:
        messages.warning(request, "You have already reported this recipe.")
        return redirect('recipe_detail', pk=recipe_pk)
    
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            description = form.cleaned_data['description']
            
            # Create the report
            report = Report.objects.create(
                reported_by=request.user,
                content_type=content_type,
                object_id=recipe_pk,
                reason=reason,
                description=description
            )
            
            # Notify the reporter
            Notification.create_report_received_notification(request.user)
            
            # Check if auto-hide threshold reached (e.g., 5 reports)
            report_count = Report.objects.filter(
                content_type=content_type,
                object_id=recipe_pk,
                status='pending'
            ).count()
            
            if report_count >= 5 and not recipe.is_hidden:
                recipe.is_hidden = True
                recipe.save()
                # Notify author
                if recipe.author != request.user:
                    Notification.create_content_removed_notification(
                        recipe.author,
                        'recipe',
                        recipe.title,
                        'Multiple user reports - pending admin review'
                    )
            
            messages.success(request, "Thank you for your report. We will review it shortly.")
            return redirect('recipe_detail', pk=recipe_pk)
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = ReportForm()
    
    # GET request or form errors - show report form
    return render(request, 'report_content.html', {
        'form': form,
        'content_type': 'recipe',
        'content_preview': f"{recipe.title} by {recipe.author.get_full_name()}",
        'cancel_url': reverse('recipe_detail', kwargs={'pk': recipe_pk})
    })


@login_required
def report_comment(request, comment_pk):
    """Report a comment for inappropriate content."""
    comment = get_object_or_404(Comment, pk=comment_pk)
    
    # Prevent staff/superusers from reporting
    if request.user.is_staff or request.user.is_superuser:
        messages.error(request, "Staff members cannot submit reports.")
        return redirect('recipe_detail', pk=comment.recipe.pk)
    
    # Prevent reporting own content
    if comment.user == request.user:
        messages.error(request, "You cannot report your own comment.")
        return redirect('recipe_detail', pk=comment.recipe.pk)
    
    # Check if user already reported this comment
    content_type = ContentType.objects.get_for_model(Comment)
    existing_report = Report.objects.filter(
        reported_by=request.user,
        content_type=content_type,
        object_id=comment_pk
    ).exists()
    
    if existing_report:
        messages.warning(request, "You have already reported this comment.")
        return redirect('recipe_detail', pk=comment.recipe.pk)
    
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            description = form.cleaned_data['description']
            
            # Create the report
            report = Report.objects.create(
                reported_by=request.user,
                content_type=content_type,
                object_id=comment_pk,
                reason=reason,
                description=description
            )
            
            # Notify the reporter
            Notification.create_report_received_notification(request.user)
            
            # Check if auto-hide threshold reached (e.g., 3 reports for comments)
            report_count = Report.objects.filter(
                content_type=content_type,
                object_id=comment_pk,
                status='pending'
            ).count()
            
            if report_count >= 3 and not comment.is_hidden:
                comment.is_hidden = True
                comment.save()
                # Notify author
                if comment.user != request.user:
                    Notification.create_content_removed_notification(
                        comment.user,
                        'comment',
                        comment.text[:50],
                        'Multiple user reports - pending admin review'
                    )
            
            messages.success(request, "Thank you for your report. We will review it shortly.")
            return redirect('recipe_detail', pk=comment.recipe.pk)
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = ReportForm()
    
    # GET request or form errors - show report form
    return render(request, 'report_content.html', {
        'form': form,
        'content_type': 'comment',
        'content_preview': comment.text,
        'cancel_url': reverse('recipe_detail', kwargs={'pk': comment.recipe.pk})
    })

