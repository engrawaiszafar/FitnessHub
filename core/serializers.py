from django.contrib.auth.models import User
from rest_framework import serializers
from .models import (
    Exercise,
    WorkoutSet,
    DietLog,
    FoodItem
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model, used for registration."""

    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a new user with an encrypted password."""
        return User.objects.create_user(**validated_data)


# --- NEW WORKOUT 2.0 SERIALIZERS ---

class ExerciseSerializer(serializers.ModelSerializer):
    """Serializer for the Exercise model."""

    class Meta:
        model = Exercise
        fields = ['id', 'user', 'name', 'muscle_group']
        read_only_fields = ['user']


class WorkoutSetSerializer(serializers.ModelSerializer):
    """Serializer for the WorkoutSet model."""
    # We include 'exercise_name' to make it easy for the frontend
    # to display the name of the exercise without a separate API call.
    exercise_name = serializers.CharField(source='exercise.name', read_only=True)

    class Meta:
        model = WorkoutSet
        fields = [
            'id', 'user', 'exercise', 'exercise_name',
            'date', 'reps', 'weight'
        ]
        read_only_fields = ['user']
        # 'exercise' will be write-only (we pass an ID)
        # 'exercise_name' will be read-only


# --- UNCHANGED DIET SERIALIZERS ---

class FoodItemSerializer(serializers.ModelSerializer):
    """Serializer for the FoodItem model."""

    class Meta:
        model = FoodItem
        fields = ['id', 'meal_type', 'name', 'calories']


class DietLogSerializer(serializers.ModelSerializer):
    """Serializer for the daily DietLog. It includes its related food items."""
    food_items = FoodItemSerializer(many=True, read_only=True)

    class Meta:
        model = DietLog
        fields = ['id', 'user', 'date', 'food_items']
        read_only_fields = ['user']
