"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
import os
from django.http import JsonResponse

router = DefaultRouter()
router.register(r'users', views.UserProfileViewSet, basename='users')
router.register(r'teams', views.TeamViewSet, basename='teams')
router.register(r'activities', views.ActivityViewSet, basename='activities')
router.register(r'workouts', views.WorkoutViewSet, basename='workouts')
router.register(r'leaderboard', views.LeaderboardEntryViewSet, basename='leaderboard')

# API root with dynamic Codespace URL
def api_root(request):
    codespace_name = os.environ.get('CODESPACE_NAME', '')
    base_url = f"https://{codespace_name}-8000.app.github.dev" if codespace_name else "http://localhost:8000"
    return JsonResponse({
        'users': f'{base_url}/api/users/',
        'teams': f'{base_url}/api/teams/',
        'activities': f'{base_url}/api/activities/',
        'workouts': f'{base_url}/api/workouts/',
        'leaderboard': f'{base_url}/api/leaderboard/',
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
