"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'users', views.UserProfileViewSet, basename='users')
router.register(r'teams', views.TeamViewSet, basename='teams')
router.register(r'activities', views.ActivityViewSet, basename='activities')
router.register(r'workouts', views.WorkoutViewSet, basename='workouts')
router.register(r'leaderboard', views.LeaderboardEntryViewSet, basename='leaderboard')

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
