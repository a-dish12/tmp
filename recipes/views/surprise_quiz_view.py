from django.shortcuts import render, redirect
from recipes.forms.surpriseme_form import SurpriseMeForm
from recipes.views.dashboard_view import DashboardView
from django.urls import reverse

def surprise_quiz_view(request):
    form = SurpriseMeForm(request.GET or None)

    if form.is_valid() and request.GET:
        return redirect(f"{reverse('surprise-result')}?{request.GET.urlencode()}")
    
    return render(request, "surprise-quiz.html", {"form":form})