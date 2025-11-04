# core/models.py
from django.db import models
from django.contrib.auth.models import User

# --- WORKOUT PLANNER MODELS ---
# Replaces: workoutPlan_[user]

class DailyWorkout(models.Model):
    """
    Represents a single day's workout plan for a user.
    """
    DAY_CHOICES = [
        (0, 'Sunday'),
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_workouts')
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    focus = models.CharField(max_length=255, blank=True, null=True, help_text="e.g., 'Chest, Back, Legs'")
    exercises = models.TextField(blank=True, null=True, help_text="e.g., Bench Press\n3 sets x 8-10 reps")

    class Meta:
        # Ensures a user can only have one plan per day
        unique_together = ('user', 'day_of_week')

    def __str__(self):
        return f"{self.user.username}'s {self.get_day_of_week_display()} Workout"


# --- DIET PLANNER MODELS ---
# Replaces: dietPlan_[user]_[date]

class DietLog(models.Model):
    """
    Represents a single day's diet log for a user.
    This will be the parent for all food items on a specific date.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diet_logs')
    date = models.DateField()

    class Meta:
        # Ensures a user can only have one diet log per day
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.username}'s Diet Log for {self.date}"

class FoodItem(models.Model):
    """
    Represents a single food item within a meal, linked to a DietLog.
    """
    MEAL_CHOICES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Snacks', 'Snacks'),
    ]

    diet_log = models.ForeignKey(DietLog, on_delete=models.CASCADE, related_name='food_items')
    meal_type = models.CharField(max_length=50, choices=MEAL_CHOICES)
    name = models.CharField(max_length=200)
    calories = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.calories} kcal) for {self.diet_log.user.username}"