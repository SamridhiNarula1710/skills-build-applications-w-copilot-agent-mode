from django.conf import settings
from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    display_name = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    joined_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.display_name or str(self.user)


class Team(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(UserProfile, related_name='teams', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class Activity(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=120)
    duration_minutes = models.PositiveIntegerField(default=0)
    distance_km = models.FloatField(null=True, blank=True)
    calories_burned = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'activities'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.activity_type} by {self.user}"


class Workout(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    difficulty = models.CharField(max_length=50, default='medium')
    duration_minutes = models.PositiveIntegerField(default=30)
    exercises = models.JSONField(blank=True, default=list)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'workouts'
        ordering = ['title']

    def __str__(self):
        return self.title


class LeaderboardEntry(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='leaderboard_entries')
    points = models.PositiveIntegerField(default=0)
    rank = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['-points', 'rank']

    def __str__(self):
        return f"{self.user} - {self.points} points"
