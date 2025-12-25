from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from recipes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/following/', views.DashboardView.as_view(), name='following_dashboard'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('recipes/create/', views.CreateRecipeView.as_view(), name='create_recipe'),
    path('recipes/<int:pk>/edit/', views.EditRecipeView.as_view(), name='edit_recipe'),
    path('recipes/<int:pk>/delete/', views.DeleteRecipeView.as_view(), name='delete_recipe'),
    path('recipes/my-recipes/', views.UserRecipesView.as_view(), name='user_recipes'),
    path('users/<int:user_id>/', views.user_profile, name='user_profile'),
    path('users/<int:user_id>/follow/', views.follow_user, name = 'follow_user'),
    path('users/<int:user_id>/unfollow/', views.unfollow_user, name = 'unfollow_user'),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipes/<int:recipe_pk>/rate/', views.RateRecipeView.as_view(), name='rate_recipe'),
    path("user/<int:user_id>/followers/", views.user_followers, name="user_followers"),
    path("user/<int:user_id>/following/", views.user_following, name="user_following"),
    path("dashboard/surprise/", views.surprise_recipe_view, name="dashboard-surprise"),
    path('users/<int:user_id>/cancel-follow-request/',views.cancel_follow_request,name='cancel_follow_request'),
    path('follow-requests/<int:request_id>/accept/',views.accept_follow_request,name='accept_follow_request'),
    path('follow-requests/<int:request_id>/reject/',views.reject_follow_request, name='reject_follow_request'),
    path('recipes/<int:recipe_pk>/add-to-planner/', views.add_to_planner, name='add_to_planner'),
    path('planned-meals/<int:meal_pk>/remove/', views.remove_from_planner, name='remove_from_planner'),
    path('recipes/<int:recipe_pk>/comments/add/', views.add_comment, name='add_comment'),
    path('comments/<int:comment_pk>/reply/', views.add_reply, name='add_reply'),
    path('comments/<int:comment_pk>/delete/', views.delete_comment, name='delete_comment'),
    path("planner/range/", views.planner_range, name="planner_range"),
    path('planner/ingredients-list/', views.ingredients_list, name='ingredients_list'),
    path('planner/<str:date>/', views.planner_day, name='planner_day'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

