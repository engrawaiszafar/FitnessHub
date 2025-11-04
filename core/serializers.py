# core/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import DailyWorkout, DietLog, FoodItem


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model, used for registration."""
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a new user with an encrypted password."""
        return User.objects.create_user(**validated_data)


class FoodItemSerializer(serializers.ModelSerializer):
    """Serializer for the FoodItem model."""
    class Meta:
        model = FoodItem
        fields = ['id', 'meal_type', 'name', 'calories']
        # diet_log is handled automatically when we nest this serializer


class DietLogSerializer(serializers.ModelSerializer):
    """Serializer for the daily DietLog. It includes its related food items."""
    # This 'food_items' field will nest the FoodItemSerializer
    # 'many=True' means it can handle multiple food items
    # 'read_only=True' means it will be included when reading a DietLog,
    # but we'll use a different endpoint to create/delete food items.
    food_items = FoodItemSerializer(many=True, read_only=True)

    class Meta:
        model = DietLog
        fields = ['id', 'user', 'date', 'food_items']
        # Make the 'user' field read-only. We will set it
        # automatically in the view based on the logged-in user.
        read_only_fields = ['user']


class DailyWorkoutSerializer(serializers.ModelSerializer):
    """Serializer for the DailyWorkout model."""
    class Meta:
        model = DailyWorkout
        fields = ['id', 'user', 'day_of_week', 'focus', 'exercises']
        read_only_fields = ['user']
