from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Activity, LeaderboardEntry, Team, UserProfile, Workout


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'user',
            'username',
            'email',
            'display_name',
            'bio',
            'joined_at',
            'updated_at',
        ]
        read_only_fields = ['joined_at', 'updated_at']


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'members', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = [
            'id',
            'user',
            'activity_type',
            'duration_minutes',
            'distance_km',
            'calories_burned',
            'timestamp',
        ]
        read_only_fields = ['timestamp']


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = [
            'id',
            'title',
            'description',
            'difficulty',
            'duration_minutes',
            'exercises',
            'created_at',
        ]
        read_only_fields = ['created_at']


class LeaderboardEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaderboardEntry
        fields = ['id', 'user', 'points', 'rank', 'updated_at']
        read_only_fields = ['updated_at']
